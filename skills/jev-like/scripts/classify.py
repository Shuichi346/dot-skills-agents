"""Run choice, noul, and score decisions against a local Jeff-Qwen3.5-2B server."""

import argparse
import hashlib
import ipaddress
import json
import math
import os
import platform
import shlex
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

MODEL = "jeff-qwen3.5-2b"


def user_path(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    if platform.system() != "Windows" and "\\ " in value:
        parts = shlex.split(value)
        if len(parts) != 1:
            raise ValueError("Ambiguous escaped path; provide a single quoted or unescaped path")
        value = parts[0]
    return Path(value).expanduser().resolve()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON object key")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("Nonfinite JSON number")


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"),
                      object_pairs_hook=unique_object, parse_constant=reject_constant)


def digest(value):
    encoded = json.dumps(value, ensure_ascii=False, allow_nan=False,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def numeric(value):
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value)


def descriptive(value):
    return isinstance(value, str) and bool(value.strip())


def option_count(question):
    return 2 if question["type"] == "noul" else len(question["criteria"])


def validate_task(task, records):
    if not isinstance(task, dict) or not isinstance(task.get("name"), str) or not task["name"].strip():
        raise ValueError("Task requires a nonempty name")
    if set(task) - {"name", "questions", "review_probability_below", "runtime"}:
        raise ValueError("Unknown task configuration fields")
    questions = task.get("questions")
    if not isinstance(questions, dict) or not questions:
        raise ValueError("Task requires at least one question")
    for key, question in questions.items():
        if not descriptive(key) or not isinstance(question, dict):
            raise ValueError("Each question requires an ID and object definition")
        if set(question) - {"type", "instructions", "criteria"}:
            raise ValueError("Unknown question configuration fields")
        kind = question.get("type")
        if kind not in ("choice", "noul", "score"):
            raise ValueError("Question type must be choice, noul, or score")
        if not descriptive(question.get("instructions")):
            raise ValueError("Question instructions are required")
        criteria = question.get("criteria")
        if kind == "choice":
            if not isinstance(criteria, dict) or len(criteria) < 2:
                raise ValueError("Each choice requires at least two descriptive candidates")
            for option, definition in criteria.items():
                if not descriptive(option) or not descriptive(definition):
                    raise ValueError("Candidates require nonnumeric keys and explicit descriptions")
                try:
                    float(option)
                except ValueError:
                    continue
                raise ValueError("Choice candidate keys must not be numeric")
        elif kind == "noul":
            if criteria is not None and (not isinstance(criteria, dict)
                    or set(criteria) - {"true", "false"}
                    or any(not descriptive(value) for value in criteria.values())):
                raise ValueError("Noul criteria may describe only true and false")
        elif (not isinstance(criteria, list) or not 2 <= len(criteria) <= 10
                or any(not descriptive(level) for level in criteria)):
            raise ValueError("Score criteria require an ordered list of two to ten descriptive levels")
    threshold = task.get("review_probability_below")
    if threshold is not None and (not numeric(threshold) or not 0 <= threshold <= 1):
        raise ValueError("Review threshold must be null or a number from zero to one")
    runtime = task.get("runtime", {})
    if not isinstance(runtime, dict) or set(runtime) - {"repository_commit", "checkpoint_revision"}:
        raise ValueError("Runtime accepts only repository_commit and checkpoint_revision")
    if any(v is not None and (not isinstance(v, str) or not v.strip()) for v in runtime.values()):
        raise ValueError("Known runtime revisions must be nonempty strings")
    if not isinstance(records, list) or not records:
        raise ValueError("Input requires a nonempty records array")
    seen = set()
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("id"), str) or not record["id"].strip():
            raise ValueError("Each record requires a nonempty string ID")
        if record["id"] in seen:
            raise ValueError("Duplicate record ID")
        seen.add(record["id"])
        state = record.get("state")
        if not isinstance(state, (str, dict, list)) or not state or (isinstance(state, str) and not state.strip()):
            raise ValueError("Each record requires nonempty text, object, or array state")
        if any(not isinstance(record.get(k, ""), str) for k in ("label", "source")):
            raise ValueError("Record label and source must be strings")


class LocalApi:
    def __init__(self, base_url, timeout):
        parsed = urllib.parse.urlsplit(base_url)
        host = parsed.hostname or ""
        try:
            local = ipaddress.ip_address(host).is_loopback
        except ValueError:
            local = host.lower() == "localhost"
        if (not local or parsed.scheme not in {"http", "https"} or parsed.username
                or parsed.password or parsed.query or parsed.fragment or parsed.path not in {"", "/"}):
            raise ValueError("Use a loopback HTTP(S) base URL without credentials or a path")
        self.base = base_url.rstrip("/")
        self.timeout = timeout
        # Disable proxies and redirects so local evidence stays on the selected endpoint.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())

    def request(self, route, payload=None):
        data = None if payload is None else json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        token = os.environ.get("JEFF_API_KEY")
        if token:
            headers["Authorization"] = "Bearer " + token
        req = urllib.request.Request(self.base + route, data=data, headers=headers)
        for attempt in range(3):
            try:
                with self.opener.open(req, timeout=self.timeout) as response:
                    return json.loads(response.read().decode("utf-8"),
                                      object_pairs_hook=unique_object, parse_constant=reject_constant)
            except urllib.error.HTTPError as error:
                if error.code in {429, 503, 529} and attempt < 2:
                    error.close()
                    time.sleep(attempt + 1)
                    continue
                code = error.code
                error.close()
                raise RuntimeError(f"Jeff HTTP {code}; inspect the server and request definition") from None
            except (urllib.error.URLError, TimeoutError, OSError):
                raise RuntimeError("Jeff connection failed or timed out") from None


def validate_probabilities(probabilities, keys):
    if not isinstance(probabilities, dict) or set(probabilities) != set(keys):
        raise ValueError("Response candidate coverage does not match the task")
    if any(not numeric(p) or not 0 <= p <= 1 for p in probabilities.values()):
        raise ValueError("Invalid candidate probability")
    if not math.isclose(math.fsum(probabilities.values()), 1, abs_tol=1e-5):
        raise ValueError("Candidate probabilities do not sum to one")


def normalize_response(response, task):
    if not isinstance(response, dict) or response.get("model") != MODEL:
        raise ValueError("Response model does not match the required base model")
    answers = response.get("answers")
    if not isinstance(answers, dict) or set(answers) != set(task["questions"]):
        raise ValueError("Response question IDs do not match the task")
    decisions = {}
    for key, question in task["questions"].items():
        answer = answers[key]
        kind = question["type"]
        if not isinstance(answer, dict) or answer.get("type") != kind:
            raise ValueError("Response type does not match the question")
        decision = {"type": kind}
        if kind == "noul":
            positive = answer.get("noul")
            if not numeric(positive) or not 0 <= positive <= 1:
                raise ValueError("Noul must return a true probability from zero to one")
            # The native noul answer supplies only P(true); derive the complementary probability.
            probabilities = {"false": 1 - positive, "true": positive}
            decision.update(true_probability=positive, false_probability=1 - positive,
                            probabilities=probabilities)
        else:
            criteria = question["criteria"]
            keys = criteria if kind == "choice" else [str(i) for i in range(len(criteria))]
            probabilities = answer.get("probabilities")
            validate_probabilities(probabilities, keys)
            confidence = answer.get("confidence")
            if confidence is not None and (not numeric(confidence) or not 0 <= confidence <= 1):
                raise ValueError("Invalid confidence value")
            decision.update(confidence=confidence, probabilities=probabilities)
            if kind == "choice":
                selected = answer.get("choice")
                if (not isinstance(selected, str) or selected not in probabilities
                        or probabilities[selected] < max(probabilities.values()) - 1e-7):
                    raise ValueError("Selected candidate is not at the maximum probability")
                other = max((c for c in criteria if c != selected), key=probabilities.get)
                decision.update(selected=selected, selected_probability=probabilities[selected],
                                runner_up=other, runner_up_probability=probabilities[other],
                                margin=probabilities[selected] - probabilities[other])
            else:
                legend = {str(i): level for i, level in enumerate(criteria)}
                if answer.get("legend") != legend:
                    raise ValueError("Score legend does not match the ordered task levels")
                score = answer.get("score")
                expected = math.fsum(i * probabilities[str(i)] for i in range(len(criteria)))
                if (not numeric(score) or not 0 <= score <= len(criteria) - 1
                        or not math.isclose(score, expected, rel_tol=1e-5, abs_tol=1e-5)):
                    raise ValueError("Score does not match the expected level index")
                decision.update(score=score, legend=legend)
        decision["dominant_probability"] = max(probabilities.values())
        threshold = task.get("review_probability_below")
        if threshold is not None:
            decision["below_review_threshold"] = decision["dominant_probability"] < threshold
        decisions[key] = decision
    usage = response.get("usage")
    if isinstance(usage, dict) and usage.get("output_tokens", 0) != 0:
        raise ValueError("Unexpected generated output tokens from the decision endpoint")
    return decisions


def question_summary(question, decisions):
    kind = question["type"]
    summary = {"type": kind, "count": len(decisions)}
    if kind == "choice":
        summary["counts"] = {candidate: sum(d["selected"] == candidate for d in decisions)
                             for candidate in question["criteria"]}
    elif kind == "noul":
        summary["mean_true_probability"] = (math.fsum(d["true_probability"] for d in decisions)
                                            / len(decisions)) if decisions else None
    else:
        summary.update(scale_min=0, scale_max=len(question["criteria"]) - 1,
                       mean_score=(math.fsum(d["score"] for d in decisions)
                                   / len(decisions)) if decisions else None)
    return summary


def checkpoint(path, report):
    report["updated_at"] = datetime.now(timezone.utc).isoformat()
    results = report["results"]
    report["summary"] = {
        "total": len(results),
        "successful": sum(r["status"] == "ok" for r in results),
        "failed": sum(r["status"] == "error" for r in results),
        "not_processed": sum(r["status"] == "not_processed" for r in results),
        "questions": {key: question_summary(q, [r["decisions"][key] for r in results if r["status"] == "ok"])
                      for key, q in report["task"]["questions"].items()},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    name = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
            name = tmp.name
            json.dump(report, tmp, ensure_ascii=False, allow_nan=False, indent=2)
            tmp.write("\n")
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(name, path)
    finally:
        if name and Path(name).exists():
            Path(name).unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, type=user_path)
    parser.add_argument("--inputs", required=True, type=user_path)
    parser.add_argument("--output", required=True, type=user_path)
    parser.add_argument("--base-url", default="http://127.0.0.1:8765")
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if sys.prefix == sys.base_prefix:
        raise ValueError("Run this helper with a dedicated virtual-environment interpreter")
    if args.output in {args.task, args.inputs}:
        raise ValueError("Output must not replace task or input files")
    if not math.isfinite(args.timeout) or args.timeout <= 0 or (args.limit is not None and args.limit < 1):
        raise ValueError("Timeout and optional limit must be positive")
    task = load_json(args.task)
    inputs = load_json(args.inputs)
    records = inputs.get("records") if isinstance(inputs, dict) else None
    validate_task(task, records)
    if args.limit is not None:
        records = records[:args.limit]
    api = LocalApi(args.base_url, args.timeout)
    health = api.request("/health")
    available = api.request("/v1/models")
    if health.get("status") != "ready" or health.get("model") != MODEL or health.get("merged_adapter"):
        raise ValueError("A ready Jeff-Qwen3.5-2B base server is required")
    if MODEL not in {m.get("name") for m in available.get("models", [])}:
        raise ValueError("Required model is not advertised by the server")
    limit = health.get("max_options")
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 2:
        raise ValueError("Server did not advertise a valid candidate limit")
    if any(option_count(q) > limit for q in task["questions"].values()):
        raise ValueError("Task exceeds the active checkpoint's candidate limit")
    inventory = [{"id": r["id"], "label": r.get("label", r["id"]), "source": r.get("source", ""),
                  "input_sha256": digest(r["state"])} for r in records]
    fingerprint = digest([task, inventory, api.base, MODEL, limit])
    if args.output.exists():
        if not args.resume:
            raise ValueError("Output already exists; use a new filename or --resume")
        report = load_json(args.output)
        if report.get("schema_version") not in (1, 2):
            raise ValueError("Unsupported resume report schema")
        if report.get("fingerprint") != fingerprint or report.get("inventory") != inventory:
            raise ValueError("Resume task, input inventory, or endpoint mismatch")
        if [r.get("id") for r in report.get("results", [])] != [r["id"] for r in inventory]:
            raise ValueError("Resume result inventory mismatch")
        for result in report["results"]:
            if result.get("status") == "ok":
                result["decisions"] = normalize_response(result["raw_response"], task)
    else:
        if args.resume:
            raise ValueError("Resume output does not exist")
        report = {"schema_version": 2, "created_at": datetime.now(timezone.utc).isoformat(),
                  "fingerprint": fingerprint, "task": task, "inventory": inventory,
                  "runtime": {"os": platform.system(), "architecture": platform.machine(),
                              "endpoint": api.base + "/v1/systemone", "model": MODEL,
                              "max_options": limit, **task.get("runtime", {})},
                  "results": [{**item, "status": "not_processed"} for item in inventory]}
    report["schema_version"] = 2
    checkpoint(args.output, report)
    consecutive_errors = 0
    for i, record in enumerate(records):
        if report["results"][i].get("status") == "ok":
            continue
        start = time.perf_counter()
        item = {**inventory[i]}
        try:
            response = api.request("/v1/systemone", {"model": MODEL, "state": record["state"],
                                                     "questions": task["questions"], "orders": 1})
            item.update(status="ok", decisions=normalize_response(response, task),
                        raw_response=response, usage=response.get("usage"))
            consecutive_errors = 0
        except (ValueError, RuntimeError, KeyError, TypeError) as error:
            item.update(status="error", error=str(error))
            consecutive_errors += 1
        item["elapsed_seconds"] = round(time.perf_counter() - start, 4)
        report["results"][i] = item
        checkpoint(args.output, report)
        print(f"{i + 1}/{len(records)}: {item['status']}", flush=True)
        if consecutive_errors >= 3:
            print("Stopped after three consecutive errors; inspect failures before resuming.", file=sys.stderr)
            break
    print(json.dumps(report["summary"], ensure_ascii=False), flush=True)
    return 0 if report["summary"]["successful"] == len(records) else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, OSError, KeyError, TypeError) as failure:
        print(f"Classification stopped: {failure}", file=sys.stderr)
        raise SystemExit(2) from None

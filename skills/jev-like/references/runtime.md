# Local runtime

Check the current [repository](https://github.com/firelex/jeff), [pyproject.toml](https://github.com/firelex/jeff/blob/main/pyproject.toml), [server](https://github.com/firelex/jeff/blob/main/src/jeff/server.py), and [model card](https://huggingface.co/mstrasser/Jeff-Qwen3.5-2B) before a new installation. APIs and supported dependency versions can change. The repository currently promotes a different, smaller model in its quick start; retain the requested 2B checkpoint.

## Environment and backend

Detect `platform.system()` and `platform.machine()` using an existing virtual-environment interpreter, or inspect OS and architecture with native shell commands before creating one. Run `python --version` / `py --version` as appropriate and check the selected revision's Python requirement. Current Jeff requires Python 3.12 or newer. Check that `uv` meets the repository's requirement when using its lockfile.

All setup paths below are relative to a writable task workspace. Replace the example directory names with suitable local directories. Do not write environments or model weights into the installed skill folder.

### Apple Silicon macOS

```sh
git clone https://github.com/firelex/jeff.git jeff-runtime
cd jeff-runtime
uv venv .venv --python 3.12
uv sync --no-default-groups --extra mac
uv run --no-default-groups --extra mac hf download mstrasser/Jeff-Qwen3.5-2B --local-dir checkpoints/Jeff-Qwen3.5-2B
JEFF_CHECKPOINT=checkpoints/Jeff-Qwen3.5-2B JEFF_BACKEND=mlx JEFF_HOST=127.0.0.1 PORT=8765 uv run --no-default-groups --extra mac jeff-serve
```

`uv sync` uses the clone's `.venv`; confirm `sys.prefix != sys.base_prefix` in the chosen interpreter. Use `.venv/bin/python` for helper scripts. Do not install the training/default dependency groups just to serve. MLX is for Apple Silicon, not Intel Macs or Windows.

### Windows PowerShell

```powershell
git clone https://github.com/firelex/jeff.git jeff-runtime
Set-Location jeff-runtime
uv venv .venv --python 3.12
uv sync --no-default-groups
uv run --no-default-groups hf download mstrasser/Jeff-Qwen3.5-2B --local-dir checkpoints/Jeff-Qwen3.5-2B
$env:JEFF_CHECKPOINT = 'checkpoints/Jeff-Qwen3.5-2B'
$env:JEFF_BACKEND = 'pytorch'
$env:JEFF_DEVICE = 'cpu'
$env:JEFF_HOST = '127.0.0.1'
$env:PORT = '8765'
uv run --no-default-groups jeff-serve
```

Use `.venv\Scripts\python.exe` for helper scripts. Do not use POSIX activation or inline environment-assignment syntax in PowerShell. The CPU route avoids assuming a particular GPU. Inspect compatible upstream dependency wheels before downloading a large checkpoint; if native Windows is unsupported for the selected revision, report the specific dependency and ask about an available WSL environment rather than silently switching systems or models.

### Intel macOS

Use the macOS shell steps without `--extra mac`, with `JEFF_BACKEND=pytorch` and `JEFF_DEVICE=cpu`. Use `.venv/bin/python`. CPU execution may be slower; measure a representative pilot instead of promising a latency.

If `uv` is unavailable, create `.venv` with `python -m venv .venv` or `py -3.12 -m venv .venv`, then use its interpreter to install the clone with `-m pip install .` (`-m pip install '.[mac]'` on Apple Silicon). Keep every Python operation in this environment and respect the selected revision's locked dependencies. Never install globally as a workaround.

## Revisions and service checks

- Prefer a known compatible release or immutable commit when setting up; record `git rev-parse HEAD`. Resolve and record the Hugging Face checkpoint revision when available and use `hf download --revision` for reproducibility. Do not invent a revision for an existing server.
- Verify the checkpoint contains `decision_config.json`, `readout.safetensors`, tokenizer/configuration files, and model weights. A normal Qwen model or GGUF alone does not include Jeff's decision readout.
- Keep `JEFF_ADAPTERS` unset for this base-model workflow. Do not copy 0.8B adapters onto the 2B base or alter the checkpoint's prompt layout/temperature.
- Confirm `GET /health` reports ready, base model `jeff-qwen3.5-2b`, and the supported option limit. Confirm the same model is advertised by `GET /v1/models`. If authentication is enabled, use an environment variable for the bearer token and never print it.
- Bind new services to loopback. Reuse an already running server without restarting it. On another occupied port, choose a free local port and pass its URL explicitly.
- Do not hardcode an option limit from the latest model card: the active checkpoint may have an older limit. The helper reads `/health` and rejects an oversized candidate set.
- Inspect the selected version's context-length behavior. Send complete evidence; report over-limit items and obtain an agreed extraction or segmentation rule rather than truncating silently.

Jeff's native endpoint is `POST /v1/systemone`, not a chat-completions endpoint. The [server implementation](https://github.com/firelex/jeff/blob/main/src/jeff/server.py) is the authority for its request/response contract. Do not route this workflow through a generic Ollama/LM Studio generation API.

The same 2B checkpoint supports `choice`, `noul`, and `score`. These are question formats, not different models or adapters. Verify the installed server accepts the chosen formats in a pilot; do not substitute `choice` for a rejected format without resolving the API-version mismatch. The helper checks each question's effective outcome count against the active checkpoint's option limit and enforces the API's 2-to-10-level score range.

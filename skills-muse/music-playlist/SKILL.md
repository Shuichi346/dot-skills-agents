---
name: music-playlist
description: Build and play a personal music library. When asked to make a playlist (「〜の曲のプレイリスト作って」 or a track list), download the songs audio-only from YouTube with yt-dlp into that playlist's own folder (files named "Artist - Title.m4a") and create that playlist's own embedded player page. When asked later to hear a song (「あの曲聴きたい」「〜再生して」), present that track in the chat so it plays on the spot. PRIVATE, personal use only — never publish the audio or any link to it.
---

# Music Playlist

Two jobs, one library:

1. **Make a playlist** — an artist or theme is named, with a track list (「〜の曲のプレイリスト作って」). Download the songs into the library folder.
2. **Play it later** — days later, a song is requested. Find it in the library and put it in the chat so it plays right there.

## Privacy — read first

- This is a **personal** library. **Never publish it**: no public web artifacts, no uploads to public file hosting, no shared links.
- Playback happens inside the owner's own environment, two ways: a single song is attached in the chat on request, and each playlist is browsable in its own private in-app player page (below). There is no ZIP handoff.

## Requirements and setup — check before the first playlist

This setup assumes a Muse environment like the one this skill was developed in: a Linux VM whose shell runs as root and whose home directory persists across VM replacements, while files outside the home directory may be wiped. Two consequences:

- **Do not use Homebrew** — it refuses to run as root in this environment.
- Hand-installed tools go under **`~/workspace/bin/`**, so they survive VM replacements. That directory is not on the default PATH, so call those tools by absolute path.

This skill needs four tools. Before the first playlist, check each one; if one is missing, install it by the route below, then check again. Do not start downloading until `yt-dlp` and `ffprobe` both answer.

| Tool | Used for | Where it lives in this environment | Check |
|---|---|---|---|
| yt-dlp | Downloading the audio from YouTube | `~/workspace/bin/yt-dlp` (standalone binary) | `~/workspace/bin/yt-dlp --version` |
| ffmpeg (ffprobe) | Probing durations, verifying files, converting audio that is better than the benchmark | system package (`/usr/bin/ffprobe`) | `ffprobe -version` |
| Node.js | JS runtime for yt-dlp's YouTube extraction (passed as `--js-runtimes node`) | system package (`/usr/bin/node`) | `node --version` |
| Python 3 | Running `scripts/make_catalog.py` | system package (`/usr/bin/python3`) | `python3 --version` |

Install routes (the method used to set up the original environment):

- **yt-dlp** — download the official standalone binary from the yt-dlp GitHub releases page into `~/workspace/bin/yt-dlp` and make it executable (`chmod +x`). Update it later with `~/workspace/bin/yt-dlp -U`.
- **uv** (handy for Python-side tooling) — the official astral installer, with `UV_INSTALL_DIR` pointed at `~/workspace/bin` so `uv` and `uvx` land there.
- **ffmpeg, Node.js, Python 3** — in this environment these are Debian system packages (`ffmpeg`, `nodejs`, `python3`) and are normally already present. If one is missing: `apt-get update && apt-get install -y ffmpeg nodejs python3`. Note that apt can be slow behind this environment's proxy — give the commands timeouts and retry rather than letting them hang.

## Layout — one folder per playlist

**Playlists are standalone units**: each request creates one complete playlist as its own folder. Do NOT keep adding tracks into an existing playlist as a standing style, and do not merge playlists together.

```
~/music_playlist/
  <プレイリスト名>/
    <アーティスト名> - <曲名>.m4a
    ...
```

- The library root is `~/music_playlist/`, directly under `~/`.
- A single-artist playlist organized by albums may use album subfolders inside its playlist folder.
- File name format is exactly `アーティスト名 - 曲名.m4a`, so each file is identifiable later. No track numbers in file names.

## In-app player — one player per playlist

Each playlist gets **its own** private embedded player page, holding embedded copies of **that playlist's tracks only** — an iPhone-Music-style player with title/artist/album metadata, search, filter chips, 曲／アルバム／アーティスト views, sorting, a play queue, shuffle and repeat. App pages cannot reference workspace files, so embedding is the only way an in-app page can play the songs. The playlist folder under `~/music_playlist/` holds the originals; the player page holds copies.

- A new playlist means a **new** player page for that playlist; never add another playlist's tracks into an existing player, and never grow one combined library player.
- **Never publish or share the player pages** — they stay in the owner's own environment.

### Player template (canonical — use it for every new player)

The player implementation is templated: `templates/player-template.html` in this skill folder is the single canonical player — the skill's sample （見本）: the complete player HTML code kept **without any songs** (the track catalog is a placeholder; audio is never part of the code and is only injected, per playlist, at build time). Layout, search, filter chips, 曲／グループ views, sorting, queue, shuffle/repeat, mini player and now-playing screen all live there, with the mobile layout fix (mini player never overlaps the list) and the finished visual design (warm paper palette + dark counterpart, Mincho headings, ruled rows, crimson accent) baked into its CSS. The now-playing artwork is a vinyl record — grooved black disc, accent label with the artist name, centre hole, slowly spinning while playing. Do not re-derive the player from a prose spec per playlist.

**Icons are inline SVG only — never emoji**: control glyphs written as emoji characters (🔀 ⏮ ⏸ ⏭ 🔁 🔊) render as inconsistent coloured tiles on iOS and wreck the design. The template already follows this; keep it that way in any template edit, and state it in build requests.

**Design reference:** the CSS in the template is the design standard — warm paper palette with a dark counterpart, crimson accent, Mincho headings, ruled list rows, vinyl-record artwork, number-and-rule queue rows (pale highlight and red equalizer on the playing row), and a small group label at the top of the now-playing screen. Match the template's screens; do not restyle per playlist.

To build a new playlist's player:

1. Run `scripts/make_catalog.py <プレイリストフォルダ>` (in this skill folder) to generate the catalog JSON (title, filterKey — `album` when the folder has album subfolders, else `artist` — and per-track file/title/artist/album/duration probed with ffprobe).
2. Create the playlist's own player page from the template: the template file with the `__CATALOG_JSON__` placeholder replaced by that catalog JSON and `__PLAYLIST_TITLE__` replaced by the playlist name, plus the playlist's `.m4a` files placed as assets so each catalog `file` path resolves relative to the page. Name the template file and the playlist folder in the build request so the builder starts from the template instead of designing a new player.
3. Per-playlist differences are **only** the catalog and the audio assets. Any change to the player's layout, features or behaviour is made in `templates/player-template.html` itself, so every future player inherits it; rebuild an existing player from the updated template only when asked.

## Audio quality — the default spec and how to treat sources

- The standard quality benchmark （目安／デフォルト） is: **AAC, 44.1 kHz, 128 kbps**.
- **At playlist creation, probe every downloaded file and treat it by tier**:
  - **Worse than the benchmark** (lower bitrate, lower sample rate) → **keep exactly as downloaded**. No upconversion, no "fixing".
  - **Better than the benchmark** (higher bitrate, higher sample rate, lossless or otherwise higher-tier source) → **convert down to the default**: AAC, 44.1 kHz, 128 kbps, `.m4a`.
  - **At the benchmark** → keep as-is.
- After creation, the library file is final: keep it bit-identical in chat attachments and in the player page's embedded copies. Never re-encode library files later to make a player fit — if embedding the full library makes the player heavy, report that constraint instead.

## Download

Use the local yt-dlp at `~/workspace/bin/yt-dlp` (call by absolute path). Audio only, m4a:

```
~/workspace/bin/yt-dlp --js-runtimes node --no-playlist --no-warnings \
  -f "bestaudio[ext=m4a]/bestaudio" \
  -o "<出力ファイルの絶対パス>" "ytsearch1:<アーティスト名> <曲名>"
```

- Search-based extraction (`ytsearch1:`) is the reliable route; direct per-video URL extraction is often bot-blocked. Do not stall on the block — the search route reaches the same videos.
- **A title that cannot be found is skipped, never substituted with a different song**, and reported in the skip list at the end.
- **Verify the top hit is the right song before trusting it.** The first search hit can be an album trailer, a cover, a live version, a short edit, a duet or part-2 version, a concert recording, or even another artist's same-titled song (all seen in practice). Check the selected video's title and duration (`--print "%(title)s | %(duration_string)s | %(id)s"` on the query). If it is wrong, refine the query — romanized artist name, title + album name, title in its official romanization, or + 公式 — until the first hit is the official music video or the official topic audio.
- Note: yt-dlp skips the download if the output file already exists. When re-grabbing a track, download to a temporary name (e.g. `-o "%(id)s.m4a"` in a temp folder) and move the file whose video ID matches the verified target.
- Watch for duplicates: two tracks with identical duration and identical file size/hash are almost certainly the same video grabbed twice; re-check both.
- A suspiciously short file is not automatically wrong — some tracks genuinely run about a minute — but cross-check its duration against the search listing before accepting it.
- One track at a time, in order; keep a results log (OK / SKIP per track) as you go.
- Long batches may run as a background job. **After any batch, verify the final state with a fresh listing before reporting**: background writes can materialize with delay, and an "OK" in the batch log is not proof the file is present under its final name. Re-download, in the foreground, anything the fresh listing shows as missing, and clean up duplicate or misnamed files left by the delay.
- Final check before reporting: every album's file count matches its list minus skips, and ffprobe parses every file with a plausible duration.

## Report after making a playlist

Briefly: what was downloaded (with counts), the skip list (tracks not found after retries), any track whose source video could not be confirmed as the official one, that the playlist's own player page was created, and one line on how playback works: 「聴きたい曲を言えばこのチャットで出すか、そのプレイリストのプレイヤーで聞けます」.

## Playback requests

When asked for a song in the library (「<曲名>聴きたい」「<曲名>再生して」), or for an album/artist from the library:

- Find the file under `~/music_playlist/<プレイリスト名>/…/アーティスト名 - 曲名.m4a`. If several playlists/artists match, pick the obvious one; ask only if genuinely ambiguous.
- Attach the audio file in your reply so it plays in the chat. For a whole playlist or album, attach the tracks in order (or the first track and say the rest will follow on request, if attaching all is unwieldy).
- If the song is not in the library, say so and offer to make a playlist containing it (playlists are created as standalone units; do not append it to an existing playlist).

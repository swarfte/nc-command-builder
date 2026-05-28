# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tkinter GUI tool for building netcat commands during CTF competitions. Single-file application (`main.py`) using ttkbootstrap theming.

## Run

```bash
uv run python main.py
```

Requires Python >=3.14. Dependencies managed by uv (`pyproject.toml` + `uv.lock`).

## Build (Windows exe)

```bash
uv run pyinstaller --onefile --windowed main.py
```

## Architecture

Everything lives in `main.py` (~550 lines):

- **`TEMPLATES` / `NC_FLAVORS`** — dict constants for payload templates and nc variant mappings
- **`payload_to_printf()`** — converts raw payload to printf-safe string (handles plain, escapes, hex, base64 modes)
- **`build_command()`** — assembles final shell command string from all parameters; handles flag ordering (`-p` before port in listen mode), flavor-specific behavior, and payload piped via printf/echo
- **`NcCommandBuilder(ttk.Window)`** — main GUI class, three-section layout:
  - Top bar: target host/port, mode (Connect/Listen), protocol, nc flavor
  - Middle: payload editor (left) + helper buttons and profile save/load (right)
  - Bottom: options checkboxes, command preview, copy/run buttons
- **Profiles** — JSON files in `profiles/` directory, created at runtime

## Key Design Decisions

- Default nc flavor is **GNU netcat** (not OpenBSD). Listen mode uses `-p` before port for OpenBSD/ncat but omits it for GNU.
- Payloads are piped via `printf` (preferred) or `echo -e`. The `payload_to_printf` function escapes control characters to `\x` notation.
- All tkinter variables use `trace_add("write")` to trigger live command preview updates.
- `_run_command` opens a new terminal window (`cmd /k` on Windows, `x-terminal-emulator` on Linux).

## Dependencies

- `ttkbootstrap` — themed Tkinter widgets (cosmo theme)
- `tkinterdnd2` — drag-and-drop (declared but not yet used in code)
- `pygments` — syntax highlighting (declared but not yet used in code)
- `pyinstaller` — packaging only

# Pre Action

- check log.md to see what you have done before.

# Post Action

- write down what you have done in log.md

# Session Log — nc-command-builder MVP

**Date:** 2026-05-27
**Branch:** dev

## What was built

Replaced placeholder `main.py` with a full-featured Tkinter GUI application (ttkbootstrap dark theme) for building netcat commands during CTF competitions.

## Features implemented

### Top bar — Target & Mode
- Host / Port fields
- Mode selector: Connect / Listen
- Protocol selector: TCP / UDP
- nc flavor dropdown: OpenBSD nc, GNU netcat, ncat (nmap)

### Middle — Payload Editor
- Multi-line text editor with scrollbar
- Payload type radio buttons: Plain text, Escapes, Hex input, Base64 decode
- Send method toggle: printf / echo -e
- Template selector with pre-built CTF templates:
  - Raw TCP line, HTTP GET, HTTP POST, Redis PING, SMTP HELO
- Live char/byte/line count display

### Middle — Helpers panel
- Insert CRLF (`\r\n`), `\n`, null byte (`\x00`)
- Wrap HTTP headers button
- Add blank line (double CRLF)
- Trim trailing spaces
- URL-encode payload
- Save / Load profiles (JSON files in `profiles/` directory)

### Bottom — Options & Command Preview
- Verbose (-v), No DNS (-n) checkboxes
- Timeout (-w), Close delay (-q), Bind (-s) fields
- Live command preview (read-only Consolas-styled text)
- Copy Command / Copy Payload Only buttons
- Run in Terminal button (opens new terminal window)

## Technical details

- Framework: ttkbootstrap (darkly theme)
- Zero external dependencies beyond what's in pyproject.toml
- `uv run python main.py` to launch
- Profiles saved as JSON in `profiles/` directory

## Files changed

- `main.py` — complete rewrite (329 lines)

## Testing

- Import verification passed
- GUI launched and rendered correctly
- User closed window (clean exit)

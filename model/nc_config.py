"""Configuration and constants for netcat command builder."""

import sys
from pathlib import Path

# Application directories
APP_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent.parent
RESOURCE_DIR = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else APP_DIR
PROFILES_DIR = APP_DIR / "profiles"

# URL-safe characters for encoding
_URL_SAFE = frozenset(
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    'abcdefghijklmnopqrstuvwxyz'
    '0123456789'
    '-._~/:?=&@!*,()'
)

# Payload templates
TEMPLATES = {
    "Custom": "",
    "Raw TCP line": "hello",
    "HTTP GET": r"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n",
    "HTTP POST": (
        r"POST / HTTP/1.1\r\n"
        r"Host: {host}\r\n"
        r"Content-Type: application/x-www-form-urlencoded\r\n"
        r"Content-Length: {length}\r\n"
        r"Connection: close\r\n\r\n"
        r"data=hello"
    ),
    "Redis PING": r"PING\r\n",
    "SMTP HELO": r"HELO localhost\r\n",
}

# Netcat flavor mappings
NC_FLAVORS = {
    "OpenBSD nc": "openbsd",
    "GNU netcat": "gnu",
    "ncat (nmap)": "ncat",
}
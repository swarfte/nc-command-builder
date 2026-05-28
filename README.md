# nc-command-builder

A GUI tool for visually constructing `netcat` commands. Built for CTF players, pentesters, and anyone tired of looking up nc flags.

![Screenshot](screenshot/main_screen.png)

## Features

- **Visual command builder** — configure host, port, mode, protocol, and nc flavor through a form, get a ready-to-run command instantly
- **Payload editor** — type your payload and pipe it through `printf` or `echo -e` automatically
- **Multiple input modes** — plain text, escape sequences (`\r\n`, `\x41`), hex bytes (`41 42 43`), or base64-decoded binary
- **Built-in templates** — one-click HTTP GET/POST, Redis PING, SMTP HELO, raw TCP line
- **Helper buttons** — insert CRLF, null bytes, wrap HTTP headers, URL-encode, trim whitespace
- **nc flavor support** — generates correct flags for OpenBSD nc, GNU netcat, and ncat (nmap)
- **Profiles** — save and load full configurations as JSON files
- **Live preview** — command updates in real-time as you change any parameter
- **Run in terminal** — opens the generated command in a new terminal window

## Quick Start

### Prerequisites

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Install & Run

```bash
# Clone the repo
git clone https://github.com/Benjamin-Chau/nc-command-builder.git
cd nc-command-builder

# Install dependencies and run
uv run python main.py
```

Or with pip:

```bash
pip install ttkbootstrap pygments tkinterdnd2
python main.py
```

### Build Windows Executable

```bash
uv run pyinstaller --onefile --windowed --name "nc-command-builder" main.py
```

The executable will be in `dist/nc-command-builder.exe`.

## Usage

### Connection Setup

Configure the top bar fields:

| Field     | Options                             | Default       |
| --------- | ----------------------------------- | ------------- |
| Host      | any hostname / IP                   | `127.0.0.1` |
| Port      | any port number                     | `1337`      |
| Mode      | Connect, Listen                     | Connect       |
| Protocol  | TCP, UDP                            | TCP           |
| nc flavor | OpenBSD nc, GNU netcat, ncat (nmap) | GNU netcat    |

### Payload Editor

Write the data to send in the payload text area. Choose how it's interpreted:

- **Plain text** — literal string, special chars escaped for shell safety
- **Escapes** — interpret `\r\n`, `\x41`, etc. as escape sequences
- **Hex** — space-separated hex bytes (e.g., `48 45 4C 4C 4F`)
- **Base64 decode** — paste base64, decoded bytes get sent

Select the piping method:

- **printf** — `printf "payload" | nc ...` (recommended, more portable)
- **echo -e** — `echo -e "payload" | nc ...`

### Templates

Pick a template from the dropdown to auto-fill the payload:

| Template     | Payload                                              |
| ------------ | ---------------------------------------------------- |
| Raw TCP line | `hello`                                            |
| HTTP GET     | `GET / HTTP/1.1\r\nHost: {host}\r\n...`            |
| HTTP POST    | `POST / HTTP/1.1\r\nHost: {host}\r\n...data=hello` |
| Redis PING   | `PING\r\n`                                         |
| SMTP HELO    | `HELO localhost\r\n`                               |

### Command Options

| Option         | Flag      | Description                              |
| -------------- | --------- | ---------------------------------------- |
| Verbose        | `-v`    | Verbose output                           |
| No DNS         | `-n`    | Skip DNS resolution                      |
| Keep listening | `-k`    | Keep accepting connections (Listen mode) |
| Timeout        | `-w N`  | Connection timeout in seconds            |
| Close delay    | `-q N`  | Wait after EOF before closing            |
| Bind address   | `-s IP` | Bind to specific local address           |

### Example Output

With default settings and `hello` as payload:

```
printf "hello" | nc -v -n -w 5 127.0.0.1 1337
```

With an HTTP GET template:

```
printf "GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n" | nc -v -n -w 5 127.0.0.1 1337
```

## Profiles

Profiles store your complete configuration (host, port, payload, all options) as JSON files in the `profiles/` directory.

- **Save Profile** — prompts for a name, saves current config
- **Load Profile** — pick from saved profiles via dropdown
- **Delete Profile** — remove a saved profile with confirmation

## Tech Stack

- **Python 3.14** + **Tkinter** — GUI framework
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) — modern themed widgets (litera theme)
- **PyInstaller** — builds standalone Windows executable

## Project Structure

```
nc-command-builder/
├── main.py           # Single-file application (~600 lines)
├── profiles/         # Saved profile JSONs (created at runtime)
├── screenshot/       # App screenshots
├── pyproject.toml    # Dependencies and metadata
├── build.md          # Build instructions
└── README.md
```

## License

Apache-2.0

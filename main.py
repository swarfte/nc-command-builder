import json
import os
import shlex
import sys
import textwrap
from pathlib import Path

import ttkbootstrap as ttk
from tkinter import StringVar, BooleanVar, Text, messagebox, filedialog
from tkinter import simpledialog
from tkinter.scrolledtext import ScrolledText


# ── Constants ────────────────────────────────────────────────────────────────

APP_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
PROFILES_DIR = APP_DIR / "profiles"

TEMPLATES = {
    "Custom": "",
    "Raw TCP line": "hello",
    "HTTP GET": "GET /?flag=pwn HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n",
    "HTTP POST": (
        "POST / HTTP/1.1\r\n"
        "Host: {host}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: {length}\r\n"
        "Connection: close\r\n\r\n"
        "data=hello"
    ),
    "Redis PING": "PING\r\n",
    "SMTP HELO": "HELO localhost\r\n",
}

NC_FLAVORS = {
    "OpenBSD nc": "openbsd",
    "GNU netcat": "gnu",
    "ncat (nmap)": "ncat",
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def payload_to_printf(raw: str, mode: str) -> str:
    """Convert payload to a printf-safe string based on mode."""
    if mode == "Plain text":
        escaped = raw.replace("\\", "\\\\").replace('"', '\\"')
        return escaped
    elif mode == "Escapes (\\r\\n, \\x41)":
        return raw
    elif mode == "Hex (41 42 43)":
        hex_clean = raw.strip().replace(",", " ").split()
        parts = []
        for h in hex_clean:
            try:
                byte_val = int(h, 16)
                if byte_val < 32 or byte_val in (34, 92):
                    parts.append(f"\\x{byte_val:02x}")
                elif byte_val == 10:
                    parts.append("\\n")
                elif byte_val == 13:
                    parts.append("\\r")
                else:
                    parts.append(chr(byte_val))
            except ValueError:
                continue
        return "".join(parts)
    elif mode == "Base64 decode → send":
        import base64
        try:
            decoded = base64.b64decode(raw)
            return "".join(
                f"\\x{b:02x}" if b < 32 or b in (34, 92) else chr(b)
                for b in decoded
            )
        except Exception:
            return raw
    return raw


def build_command(
    host: str,
    port: str,
    mode: str,
    protocol: str,
    flavor: str,
    payload: str,
    payload_mode: str,
    send_method: str,
    verbose: bool,
    no_dns: bool,
    timeout: str,
    close_delay: str,
    keep_listen: bool,
    local_bind: str,
) -> str:
    """Build the final nc command string."""
    parts = []
    is_listen = mode == "Listen"
    is_udp = protocol == "UDP"
    flavor_key = NC_FLAVORS.get(flavor, "openbsd")

    # ── payload pipeline prefix ──
    payload_prefix = ""
    if payload.strip() and not is_listen:
        printf_str = payload_to_printf(payload, payload_mode)
        if send_method == "printf":
            payload_prefix = f'printf "{printf_str}" | '
        else:
            payload_prefix = f'echo -e "{printf_str}" | '

    # ── nc binary ──
    nc_bin = "ncat" if flavor_key == "ncat" else "nc"

    # ── flags ──
    flags = []
    needs_p = False
    if is_listen:
        flags.append("-l")
        if flavor_key == "gnu":
            pass  # GNU nc: -l implies -p not needed on some versions
        else:
            needs_p = True
    if verbose:
        flags.append("-v")
    if no_dns and not is_listen:
        flags.append("-n")
    if is_udp:
        flags.append("-u")
    if timeout:
        flags.extend(["-w", timeout])
    if close_delay and flavor_key == "openbsd":
        flags.extend(["-q", close_delay])
    if close_delay and flavor_key == "ncat":
        flags.extend(["-q", close_delay])
    if local_bind and is_listen:
        flags.extend(["-s", local_bind])
    if keep_listen and is_listen:
        flags.append("-k")

    # ── host/port (ensure -p sits directly before port) ──
    target = []
    if is_listen:
        if needs_p:
            target.extend(["-p", port])
        else:
            target.append(port)
    else:
        target.extend([host, port])

    cmd = payload_prefix + nc_bin + " " + " ".join(flags) + " " + " ".join(target)
    return cmd.strip()


# ── Main App ─────────────────────────────────────────────────────────────────

class NcCommandBuilder(ttk.Window):
    def __init__(self):
        super().__init__(themename="litera")
        self.title("Netcat Command Builder")
        self.geometry("960x720")
        self.minsize(800, 600)

        # ── Variables ──
        self.var_host = StringVar(value="127.0.0.1")
        self.var_port = StringVar(value="1337")
        self.var_mode = StringVar(value="Connect")
        self.var_protocol = StringVar(value="TCP")
        self.var_flavor = StringVar(value="GNU netcat")
        self.var_payload_mode = StringVar(value="Escapes (\\r\\n, \\x41)")
        self.var_send_method = StringVar(value="printf")
        self.var_verbose = BooleanVar(value=True)
        self.var_no_dns = BooleanVar(value=True)
        self.var_timeout = StringVar(value="5")
        self.var_close_delay = StringVar(value="")
        self.var_keep_listen = BooleanVar(value=True)
        self.var_local_bind = StringVar(value="")
        self.var_template = StringVar(value="Custom")

        # ── Trace updates ──
        for var in (
            self.var_host, self.var_port, self.var_mode, self.var_protocol,
            self.var_flavor, self.var_payload_mode, self.var_send_method,
            self.var_verbose, self.var_no_dns, self.var_timeout,
            self.var_close_delay, self.var_keep_listen, self.var_local_bind,
        ):
            var.trace_add("write", lambda *_: self._update_preview())

        self._build_ui()
        self._update_preview()

    # ── UI Construction ──────────────────────────────────────────────────

    def _build_ui(self):
        self._build_top_bar()
        self._build_middle()
        self._build_bottom()

    def _build_top_bar(self):
        frame = ttk.LabelFrame(self, text="Target & Mode")
        frame.pack(fill="x", padx=8, pady=(8, 4))
        inner = ttk.Frame(frame)
        inner.pack(fill="x", padx=8, pady=8)

        ttk.Label(inner, text="Host:").grid(row=0, column=0, sticky="w")
        ttk.Entry(inner, textvariable=self.var_host, width=24).grid(
            row=0, column=1, padx=4
        )

        ttk.Label(inner, text="Port:").grid(row=0, column=2, sticky="w", padx=(8, 0))
        ttk.Entry(inner, textvariable=self.var_port, width=8).grid(
            row=0, column=3, padx=4
        )

        ttk.Label(inner, text="Mode:").grid(row=0, column=4, sticky="w", padx=(8, 0))
        ttk.Combobox(
            inner, textvariable=self.var_mode,
            values=["Connect", "Listen"], state="readonly", width=8,
        ).grid(row=0, column=5, padx=4)

        ttk.Label(inner, text="Protocol:").grid(row=0, column=6, sticky="w", padx=(8, 0))
        ttk.Combobox(
            inner, textvariable=self.var_protocol,
            values=["TCP", "UDP"], state="readonly", width=5,
        ).grid(row=0, column=7, padx=4)

        ttk.Label(inner, text="nc flavor:").grid(row=0, column=8, sticky="w", padx=(8, 0))
        ttk.Combobox(
            inner, textvariable=self.var_flavor,
            values=list(NC_FLAVORS.keys()), state="readonly", width=14,
        ).grid(row=0, column=9, padx=4)

    def _build_middle(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=8, pady=4)
        frame.columnconfigure(0, weight=3)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)

        self._build_payload_editor(frame)
        self._build_helpers(frame)

    def _build_payload_editor(self, parent):
        frame = ttk.LabelFrame(parent, text="Payload")
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        inner = ttk.Frame(frame)
        inner.pack(fill="both", expand=True, padx=8, pady=8)

        # Payload type selector
        type_frame = ttk.Frame(inner)
        type_frame.pack(fill="x")
        ttk.Label(type_frame, text="Type:").pack(side="left")
        for mode in [
            "Plain text",
            "Escapes (\\r\\n, \\x41)",
            "Hex (41 42 43)",
            "Base64 decode → send",
        ]:
            ttk.Radiobutton(
                type_frame, text=mode.split("(")[0].strip(),
                variable=self.var_payload_mode, value=mode,
            ).pack(side="left", padx=4)

        # Send method
        send_frame = ttk.Frame(inner)
        send_frame.pack(fill="x", pady=(4, 0))
        ttk.Label(send_frame, text="Send via:").pack(side="left")
        ttk.Radiobutton(
            send_frame, text="printf", variable=self.var_send_method, value="printf",
        ).pack(side="left", padx=4)
        ttk.Radiobutton(
            send_frame, text="echo -e", variable=self.var_send_method, value="echo",
        ).pack(side="left", padx=4)

        # Template selector
        tmpl_frame = ttk.Frame(inner)
        tmpl_frame.pack(fill="x", pady=(4, 0))
        ttk.Label(tmpl_frame, text="Template:").pack(side="left")
        tmpl_combo = ttk.Combobox(
            tmpl_frame, textvariable=self.var_template,
            values=list(TEMPLATES.keys()), state="readonly", width=20,
        )
        tmpl_combo.pack(side="left", padx=4)
        tmpl_combo.bind("<<ComboboxSelected>>", self._on_template)

        # Text area
        self.payload_text = ScrolledText(inner, height=8, wrap="word")
        self.payload_text.pack(fill="both", expand=True, pady=(4, 0))
        self.payload_text.bind("<KeyRelease>", lambda _: self._update_preview())

        # Byte/line count
        self.count_label = ttk.Label(inner, text="Chars: 0 | Bytes: 0 | Lines: 0")
        self.count_label.pack(anchor="w", pady=(4, 0))

    def _build_helpers(self, parent):
        frame = ttk.LabelFrame(parent, text="Helpers")
        frame.grid(row=0, column=1, sticky="nsew")
        inner = ttk.Frame(frame)
        inner.pack(fill="both", expand=True, padx=8, pady=8)

        helpers = [
            ("Insert \\r\\n (CRLF)", lambda: self._insert("\\r\\n")),
            ("Insert \\n", lambda: self._insert("\\n")),
            ("Insert \\x00 (null)", lambda: self._insert("\\x00")),
            ("Wrap HTTP headers", self._wrap_http),
            ("Add blank line", lambda: self._insert("\\r\\n\\r\\n")),
            ("Trim trailing spaces", self._trim_trailing),
            ("URL-encode payload", self._url_encode),
        ]
        for text, cmd in helpers:
            ttk.Button(inner, text=text, command=cmd, width=22).pack(
                pady=2, fill="x"
            )

        ttk.Separator(inner, orient="horizontal").pack(fill="x", pady=8)

        # Profiles
        ttk.Button(inner, text="Save Profile", command=self._save_profile, width=22, bootstyle="success").pack(
            pady=2, fill="x"
        )
        ttk.Button(inner, text="Load Profile", command=self._load_profile, width=22, bootstyle="info").pack(
            pady=2, fill="x"
        )
        ttk.Button(inner, text="Delete Profile", command=self._delete_profile, width=22, bootstyle="danger").pack(
            pady=2, fill="x"
        )

    def _build_bottom(self):
        frame = ttk.LabelFrame(self, text="Command Preview")
        frame.pack(fill="x", padx=8, pady=(4, 8))
        inner = ttk.Frame(frame)
        inner.pack(fill="x", padx=8, pady=8)

        # Options row
        opts = ttk.Frame(inner)
        opts.pack(fill="x")

        ttk.Checkbutton(opts, text="Verbose (-v)", variable=self.var_verbose).pack(
            side="left", padx=4
        )
        ttk.Checkbutton(opts, text="No DNS (-n)", variable=self.var_no_dns).pack(
            side="left", padx=4
        )
        ttk.Checkbutton(opts, text="Keep listening (-k)", variable=self.var_keep_listen).pack(
            side="left", padx=4
        )

        ttk.Label(opts, text="Timeout (-w):").pack(side="left", padx=(12, 0))
        ttk.Entry(opts, textvariable=self.var_timeout, width=5).pack(side="left", padx=2)

        ttk.Label(opts, text="Close delay (-q):").pack(side="left", padx=(12, 0))
        ttk.Entry(opts, textvariable=self.var_close_delay, width=5).pack(side="left", padx=2)

        ttk.Label(opts, text="Bind (-s):").pack(side="left", padx=(12, 0))
        ttk.Entry(opts, textvariable=self.var_local_bind, width=12).pack(side="left", padx=2)

        # Command output
        self.cmd_text = Text(
            inner, height=3, wrap="word", state="disabled",
            font=("Consolas", 11), background="#1e1e1e", foreground="#d4d4d4",
        )
        self.cmd_text.pack(fill="x", pady=(8, 4))

        # Buttons
        btn_frame = ttk.Frame(inner)
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="Copy Command", command=self._copy_command, width=16).pack(
            side="left", padx=4
        )
        ttk.Button(btn_frame, text="Copy Payload Only", command=self._copy_payload, width=18).pack(
            side="left", padx=4
        )
        ttk.Button(btn_frame, text="Run in Terminal", command=self._run_command, width=16).pack(
            side="left", padx=4
        )

    # ── Callbacks ────────────────────────────────────────────────────────

    def _insert(self, text):
        self.payload_text.insert("insert", text)
        self._update_preview()

    def _wrap_http(self):
        payload = self.payload_text.get("1.0", "end-1c")
        if not payload.startswith("GET") and not payload.startswith("POST"):
            host = self.var_host.get()
            payload = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        self.payload_text.delete("1.0", "end")
        self.payload_text.insert("1.0", payload)
        self._update_preview()

    def _trim_trailing(self):
        payload = self.payload_text.get("1.0", "end-1c")
        trimmed = payload.rstrip()
        self.payload_text.delete("1.0", "end")
        self.payload_text.insert("1.0", trimmed)
        self._update_preview()

    def _url_encode(self):
        import urllib.parse
        payload = self.payload_text.get("1.0", "end-1c")
        encoded = urllib.parse.quote(payload, safe="")
        self.payload_text.delete("1.0", "end")
        self.payload_text.insert("1.0", encoded)
        self._update_preview()

    def _on_template(self, _event=None):
        name = self.var_template.get()
        template = TEMPLATES.get(name, "")
        if template:
            host = self.var_host.get()
            length = len("data=hello")
            template = template.replace("{host}", host).replace("{length}", str(length))
            if "HTTP" in name or "SMTP" in name or "Redis" in name:
                self.var_payload_mode.set("Escapes (\\r\\n, \\x41)")
            self.payload_text.delete("1.0", "end")
            self.payload_text.insert("1.0", template)
            self._update_preview()

    def _update_preview(self):
        payload = self.payload_text.get("1.0", "end-1c")

        # Update byte/char/line count
        char_count = len(payload)
        line_count = payload.count("\n") + 1 if payload else 0
        printf_str = payload_to_printf(payload, self.var_payload_mode.get())
        byte_count = len(printf_str.encode("utf-8", errors="replace"))
        self.count_label.config(
            text=f"Chars: {char_count} | Bytes: {byte_count} | Lines: {line_count}"
        )

        cmd = build_command(
            host=self.var_host.get(),
            port=self.var_port.get(),
            mode=self.var_mode.get(),
            protocol=self.var_protocol.get(),
            flavor=self.var_flavor.get(),
            payload=payload,
            payload_mode=self.var_payload_mode.get(),
            send_method=self.var_send_method.get(),
            verbose=self.var_verbose.get(),
            no_dns=self.var_no_dns.get(),
            timeout=self.var_timeout.get(),
            close_delay=self.var_close_delay.get(),
            keep_listen=self.var_keep_listen.get(),
            local_bind=self.var_local_bind.get(),
        )

        self.cmd_text.config(state="normal")
        self.cmd_text.delete("1.0", "end")
        self.cmd_text.insert("1.0", cmd)
        self.cmd_text.config(state="disabled")

    def _copy_command(self):
        cmd = self.cmd_text.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(cmd)
        self._flash_button_feedback("Command copied!")

    def _copy_payload(self):
        payload = self.payload_text.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(payload)
        self._flash_button_feedback("Payload copied!")

    def _flash_button_feedback(self, msg):
        old_title = self.title()
        self.title(f"{old_title}  —  {msg}")
        self.after(1500, lambda: self.title(old_title))

    def _run_command(self):
        cmd = self.cmd_text.get("1.0", "end-1c")
        if not cmd:
            return
        import subprocess
        import platform
        if platform.system() == "Windows":
            subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", cmd])
        else:
            subprocess.Popen(["x-terminal-emulator", "-e", "bash", "-c", cmd])

    # ── Profiles ─────────────────────────────────────────────────────────

    def _dropdown_dialog(self, title, prompt, options):
        """Show a modal dialog with a dropdown. Returns selected value or None."""
        result = [None]
        dialog = ttk.Toplevel(self)
        dialog.title(title)
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(dialog, text=prompt).pack(padx=12, pady=(12, 4))
        var = StringVar(value=options[0])
        combo = ttk.Combobox(dialog, textvariable=var, values=options,
                             state="readonly", width=30)
        combo.pack(padx=12, pady=4)

        def on_ok():
            result[0] = var.get()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(padx=12, pady=(4, 12))
        ttk.Button(btn_frame, text="OK", command=on_ok, width=8).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Cancel", command=on_cancel, width=8).pack(side="left", padx=4)

        dialog.protocol("WM_DELETE_WINDOW", on_cancel)
        # Center on parent
        dialog.geometry(f"+{self.winfo_rootx() + 100}+{self.winfo_rooty() + 100}")
        self.wait_window(dialog)
        return result[0]

    def _save_profile(self):
        name = simpledialog.askstring("Save Profile", "Profile name:", parent=self)
        if not name:
            return
        PROFILES_DIR.mkdir(exist_ok=True)
        data = {
            "host": self.var_host.get(),
            "port": self.var_port.get(),
            "mode": self.var_mode.get(),
            "protocol": self.var_protocol.get(),
            "flavor": self.var_flavor.get(),
            "payload": self.payload_text.get("1.0", "end-1c"),
            "payload_mode": self.var_payload_mode.get(),
            "send_method": self.var_send_method.get(),
            "verbose": self.var_verbose.get(),
            "no_dns": self.var_no_dns.get(),
            "timeout": self.var_timeout.get(),
            "close_delay": self.var_close_delay.get(),
            "keep_listen": self.var_keep_listen.get(),
            "local_bind": self.var_local_bind.get(),
        }
        path = PROFILES_DIR / f"{name}.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        self._flash_button_feedback(f"Profile '{name}' saved!")

    def _load_profile(self):
        if not PROFILES_DIR.exists():
            messagebox.showinfo("Load Profile", "No profiles found.")
            return
        files = list(PROFILES_DIR.glob("*.json"))
        if not files:
            messagebox.showinfo("Load Profile", "No profiles found.")
            return
        names = [f.stem for f in files]
        name = self._dropdown_dialog("Load Profile", "Select profile:", names)
        if not name:
            return
        path = PROFILES_DIR / f"{name}.json"
        with open(path) as f:
            data = json.load(f)
        self.var_host.set(data.get("host", ""))
        self.var_port.set(data.get("port", ""))
        self.var_mode.set(data.get("mode", "Connect"))
        self.var_protocol.set(data.get("protocol", "TCP"))
        self.var_flavor.set(data.get("flavor", "OpenBSD nc"))
        self.var_payload_mode.set(data.get("payload_mode", "Plain text"))
        self.var_send_method.set(data.get("send_method", "printf"))
        self.var_verbose.set(data.get("verbose", True))
        self.var_no_dns.set(data.get("no_dns", True))
        self.var_timeout.set(data.get("timeout", ""))
        self.var_close_delay.set(data.get("close_delay", ""))
        self.var_keep_listen.set(data.get("keep_listen", True))
        self.var_local_bind.set(data.get("local_bind", ""))
        self.payload_text.delete("1.0", "end")
        self.payload_text.insert("1.0", data.get("payload", ""))
        self._update_preview()
        self._flash_button_feedback(f"Profile '{name}' loaded!")

    def _delete_profile(self):
        if not PROFILES_DIR.exists():
            messagebox.showinfo("Delete Profile", "No profiles found.")
            return
        files = list(PROFILES_DIR.glob("*.json"))
        if not files:
            messagebox.showinfo("Delete Profile", "No profiles found.")
            return
        names = [f.stem for f in files]
        name = self._dropdown_dialog("Delete Profile", "Select profile to delete:", names)
        if not name:
            return
        confirm = messagebox.askyesno(
            "Delete Profile", f"Delete profile '{name}'?", parent=self,
        )
        if not confirm:
            return
        path = PROFILES_DIR / f"{name}.json"
        path.unlink()
        self._flash_button_feedback(f"Profile '{name}' deleted!")


def main():
    app = NcCommandBuilder()
    app.mainloop()


if __name__ == "__main__":
    main()

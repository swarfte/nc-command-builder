"""Helpers panel with utility buttons for payload editing."""

import ttkbootstrap as ttk


class HelpersPanel(ttk.LabelFrame):
    """Panel with helper buttons for payload editing."""

    def __init__(self, parent, main_window):
        """Initialize helpers panel.

        Args:
            parent: Parent widget
            main_window: Main window reference
        """
        super().__init__(parent, text="Helpers")
        self.main_window = main_window
        self._build_ui()

    def _build_ui(self):
        """Build helpers panel UI."""
        inner = ttk.Frame(self)
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

    def _insert(self, text):
        """Insert text at cursor position in raw mode."""
        if self.main_window.payload_editor and self.main_window.payload_editor.raw_text:
            self.main_window.payload_editor.raw_text.insert("insert", text)

    def _wrap_http(self):
        """Wrap payload as HTTP headers."""
        if self.main_window.payload_editor and self.main_window.payload_editor.raw_text:
            payload = self.main_window.payload_editor.raw_text.get("1.0", "end-1c")
            if not payload.startswith("GET") and not payload.startswith("POST"):
                host = self.main_window.var_host.get()
                payload = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
                self.main_window.payload_editor.raw_text.delete("1.0", "end")
                self.main_window.payload_editor.raw_text.insert("1.0", payload)

    def _trim_trailing(self):
        """Trim trailing spaces from raw payload."""
        if self.main_window.payload_editor and self.main_window.payload_editor.raw_text:
            payload = self.main_window.payload_editor.raw_text.get("1.0", "end-1c")
            trimmed = payload.rstrip()
            self.main_window.payload_editor.raw_text.delete("1.0", "end")
            self.main_window.payload_editor.raw_text.insert("1.0", trimmed)

    def _url_encode(self):
        """URL-encode the current payload."""
        if self.main_window.payload_editor and self.main_window.payload_editor.raw_text:
            payload = self.main_window.payload_editor.raw_text.get("1.0", "end-1c")

            if self.main_window.payload_controller:
                encoded = self.main_window.payload_controller.url_encode_payload(payload)
                self.main_window.payload_editor.raw_text.delete("1.0", "end")
                self.main_window.payload_editor.raw_text.insert("1.0", encoded)
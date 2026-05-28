"""Postman-like payload editor with 3 independent modes."""

import ttkbootstrap as ttk
from tkinter import StringVar, IntVar, scrolledtext


class PayloadEditor(ttk.LabelFrame):
    """Postman-like payload editor with Raw/GET/POST modes."""

    def __init__(self, parent, main_window):
        """Initialize payload editor.

        Args:
            parent: Parent widget
            main_window: Main window reference
        """
        super().__init__(parent, text="Payload")
        self.main_window = main_window

        # Mode-specific data
        self.raw_text = None
        self.get_rows = []
        self.post_rows = []
        self.get_path_var = None
        self.post_path_var = None
        self.post_content_type_var = None

        # Stats
        self.count_label = None

        self._build_ui()

    def _build_ui(self):
        """Build payload editor UI."""
        inner = ttk.Frame(self)
        inner.pack(fill="both", expand=True, padx=8, pady=8)

        # Mode selector
        mode_frame = ttk.Frame(inner)
        mode_frame.pack(fill="x")

        ttk.Label(mode_frame, text="Mode:").pack(side="left")
        ttk.Radiobutton(
            mode_frame, text="Raw TCP",
            variable=self.main_window.var_editor_mode, value="raw_tcp",
            command=self._switch_mode
        ).pack(side="left", padx=4)
        ttk.Radiobutton(
            mode_frame, text="GET",
            variable=self.main_window.var_editor_mode, value="get",
            command=self._switch_mode
        ).pack(side="left", padx=4)
        ttk.Radiobutton(
            mode_frame, text="POST",
            variable=self.main_window.var_editor_mode, value="post",
            command=self._switch_mode
        ).pack(side="left", padx=4)

        # Mode-specific panels
        self.mode_container = ttk.Frame(inner)
        self.mode_container.pack(fill="both", expand=True, pady=(8, 0))

        # Build mode panels
        self._build_raw_mode()
        self._build_get_mode()
        self._build_post_mode()

        # Show default mode
        self._switch_mode()

        # Payload type selector (for Raw mode)
        type_frame = ttk.Frame(inner)
        type_frame.pack(fill="x", pady=(8, 0))
        ttk.Label(type_frame, text="Type:").pack(side="left")
        for mode in [
            "Plain text",
            "Escapes (\\r\\n, \\x41)",
            "Hex (41 42 43)",
            "Base64 decode → send",
        ]:
            ttk.Radiobutton(
                type_frame, text=mode.split("(")[0].strip(),
                variable=self.main_window.var_payload_mode, value=mode,
            ).pack(side="left", padx=4)

        # Send method
        send_frame = ttk.Frame(inner)
        send_frame.pack(fill="x", pady=(4, 0))
        ttk.Label(send_frame, text="Send via:").pack(side="left")
        ttk.Radiobutton(
            send_frame, text="printf", variable=self.main_window.var_send_method, value="printf",
        ).pack(side="left", padx=4)
        ttk.Radiobutton(
            send_frame, text="echo -e", variable=self.main_window.var_send_method, value="echo",
        ).pack(side="left", padx=4)

        # Stats
        self.count_label = ttk.Label(inner, text="Chars: 0 | Bytes: 0 | Lines: 0")
        self.count_label.pack(anchor="w", pady=(4, 0))

    def _build_raw_mode(self):
        """Build Raw TCP mode panel."""
        self.raw_panel = ttk.Frame(self.mode_container)

        # Template selector
        tmpl_frame = ttk.Frame(self.raw_panel)
        tmpl_frame.pack(fill="x", pady=(0, 4))
        ttk.Label(tmpl_frame, text="Template:").pack(side="left")

        template_names = ["Custom", "Raw TCP line", "HTTP GET", "HTTP POST", "Redis PING", "SMTP HELO"]
        self.var_template = ttk.StringVar(value="Custom")
        tmpl_combo = ttk.Combobox(
            tmpl_frame, textvariable=self.var_template,
            values=template_names, state="readonly", width=20,
        )
        tmpl_combo.pack(side="left", padx=4)
        tmpl_combo.bind("<<ComboboxSelected>>", self._on_template)

        # Text area
        self.raw_text = scrolledtext.ScrolledText(self.raw_panel, height=8, wrap="word")
        self.raw_text.pack(fill="both", expand=True)
        self.raw_text.bind("<KeyRelease>", lambda _: self._on_raw_change())

    def _build_get_mode(self):
        """Build GET mode panel."""
        self.get_panel = ttk.Frame(self.mode_container)

        # Path input
        path_frame = ttk.Frame(self.get_panel)
        path_frame.pack(fill="x", pady=(0, 4))

        ttk.Label(path_frame, text="Path:").pack(side="left")
        self.get_path_var = ttk.StringVar(value="/")
        ttk.Entry(path_frame, textvariable=self.get_path_var, width=40).pack(side="left", padx=4)
        self.get_path_var.trace_add("write", lambda *_: self._on_get_change())

        # Parameters header
        header_frame = ttk.Frame(self.get_panel)
        header_frame.pack(fill="x", pady=(4, 0))

        ttk.Label(header_frame, text="Query Parameters", font=("TkDefaultFont", 10, "bold")).pack(side="left")

        # Parameters container
        self.get_params_container = ttk.Frame(self.get_panel)
        self.get_params_container.pack(fill="both", expand=True)

        # Add parameter button
        add_frame = ttk.Frame(self.get_panel)
        add_frame.pack(fill="x", pady=(4, 0))
        ttk.Button(add_frame, text="+ Add Parameter", command=lambda: self._add_get_param(), width=15).pack(side="left")

        # Initial row
        self._add_get_param()

    def _build_post_mode(self):
        """Build POST mode panel."""
        self.post_panel = ttk.Frame(self.mode_container)

        # Path and Content-Type
        header_frame = ttk.Frame(self.post_panel)
        header_frame.pack(fill="x", pady=(0, 4))

        ttk.Label(header_frame, text="Path:").pack(side="left")
        self.post_path_var = ttk.StringVar(value="/")
        ttk.Entry(header_frame, textvariable=self.post_path_var, width=30).pack(side="left", padx=4)

        ttk.Label(header_frame, text="Content-Type:").pack(side="left", padx=(8, 0))
        content_types = [
            "application/x-www-form-urlencoded",
            "application/json",
            "text/plain"
        ]
        self.post_content_type_var = ttk.StringVar(value=content_types[0])
        ttk.Combobox(
            header_frame, textvariable=self.post_content_type_var,
            values=content_types, state="readonly", width=25,
        ).pack(side="left", padx=4)
        self.post_content_type_var.trace_add("write", lambda *_: self._on_post_change())
        self.post_path_var.trace_add("write", lambda *_: self._on_post_change())

        # Body parameters header
        body_header_frame = ttk.Frame(self.post_panel)
        body_header_frame.pack(fill="x", pady=(4, 0))

        ttk.Label(body_header_frame, text="Body Parameters", font=("TkDefaultFont", 10, "bold")).pack(side="left")

        # Parameters container
        self.post_params_container = ttk.Frame(self.post_panel)
        self.post_params_container.pack(fill="both", expand=True)

        # Add parameter button
        add_frame = ttk.Frame(self.post_panel)
        add_frame.pack(fill="x", pady=(4, 0))
        ttk.Button(add_frame, text="+ Add Parameter", command=lambda: self._add_post_param(), width=15).pack(side="left")

        # Initial row
        self._add_post_param()

    def _add_get_param(self, key="", value=""):
        """Add a parameter row to GET mode."""
        row = ttk.Frame(self.get_params_container)
        row.pack(fill="x", pady=2)

        key_var = ttk.StringVar(value=key)
        value_var = ttk.StringVar(value=value)

        key_entry = ttk.Entry(row, textvariable=key_var, width=15)
        key_entry.pack(side="left", padx=2)

        value_entry = ttk.Entry(row, textvariable=value_var, width=20)
        value_entry.pack(side="left", padx=2)

        delete_btn = ttk.Button(row, text="×", command=lambda: self._remove_get_param(row), width=3)
        delete_btn.pack(side="left", padx=2)

        # Trace changes
        key_var.trace_add("write", lambda *_: self._on_get_change())
        value_var.trace_add("write", lambda *_: self._on_get_change())

        self.get_rows.append({"row": row, "key": key_var, "value": value_var})

    def _remove_get_param(self, row):
        """Remove a parameter row from GET mode."""
        row.destroy()
        self.get_rows = [r for r in self.get_rows if r["row"] != row]
        self._on_get_change()

    def _add_post_param(self, key="", value=""):
        """Add a parameter row to POST mode."""
        row = ttk.Frame(self.post_params_container)
        row.pack(fill="x", pady=2)

        key_var = ttk.StringVar(value=key)
        value_var = ttk.StringVar(value=value)

        key_entry = ttk.Entry(row, textvariable=key_var, width=15)
        key_entry.pack(side="left", padx=2)

        value_entry = ttk.Entry(row, textvariable=value_var, width=20)
        value_entry.pack(side="left", padx=2)

        delete_btn = ttk.Button(row, text="×", command=lambda: self._remove_post_param(row), width=3)
        delete_btn.pack(side="left", padx=2)

        # Trace changes
        key_var.trace_add("write", lambda *_: self._on_post_change())
        value_var.trace_add("write", lambda *_: self._on_post_change())

        self.post_rows.append({"row": row, "key": key_var, "value": value_var})

    def _remove_post_param(self, row):
        """Remove a parameter row from POST mode."""
        row.destroy()
        self.post_rows = [r for r in self.post_rows if r["row"] != row]
        self._on_post_change()

    def _switch_mode(self):
        """Switch between payload editor modes."""
        mode = self.main_window.var_editor_mode.get()

        # Hide all panels
        self.raw_panel.pack_forget()
        self.get_panel.pack_forget()
        self.post_panel.pack_forget()

        # Show selected panel
        if mode == "raw_tcp":
            self.raw_panel.pack(fill="both", expand=True)
        elif mode == "get":
            self.get_panel.pack(fill="both", expand=True)
        elif mode == "post":
            self.post_panel.pack(fill="both", expand=True)

        # Update controller
        if self.main_window.controller:
            self.main_window.controller.update_editor_mode(mode)

        # Trigger update
        self._update_preview()

    def _on_raw_change(self):
        """Handle raw text changes."""
        if self.raw_text and self.main_window.controller:
            payload = self.raw_text.get("1.0", "end-1c")
            self.main_window.controller.raw_payload = payload
            self._update_preview()

    def _on_get_change(self):
        """Handle GET parameter changes."""
        if self.main_window.controller:
            path = self.get_path_var.get()
            params = {}

            for row_data in self.get_rows:
                key = row_data["key"].get().strip()
                value = row_data["value"].get().strip()
                if key:  # Only include non-empty keys
                    params[key] = value

            self.main_window.controller.update_get_params(path=path, params=params)
            self._update_preview()

    def _on_post_change(self):
        """Handle POST parameter changes."""
        if self.main_window.controller:
            path = self.post_path_var.get()
            content_type = self.post_content_type_var.get()
            params = {}

            for row_data in self.post_rows:
                key = row_data["key"].get().strip()
                value = row_data["value"].get().strip()
                if key:  # Only include non-empty keys
                    params[key] = value

            self.main_window.controller.update_post_params(path=path, content_type=content_type, params=params)
            self._update_preview()

    def _on_template(self, event=None):
        """Handle template selection."""
        if self.main_window.payload_controller:
            template_name = self.var_template.get()
            payload, suggested_mode = self.main_window.payload_controller.apply_template(template_name)

            # Update raw text
            if self.raw_text:
                self.raw_text.delete("1.0", "end")
                self.raw_text.insert("1.0", payload.replace("\\r\\n", "\n"))

            # Update suggested mode
            self.main_window.var_payload_mode.set(suggested_mode)

            # Switch to raw mode
            self.main_window.var_editor_mode.set("raw_tcp")
            self._switch_mode()

    def _update_preview(self):
        """Update command preview and stats."""
        # Update stats
        self.update_stats()

        # Trigger main window preview update
        if self.main_window:
            self.main_window._update_preview()

    def update_stats(self):
        """Update payload statistics display."""
        if not self.count_label or not self.main_window.controller:
            return

        # Get current payload
        payload = self.main_window.controller._get_current_payload()

        if self.main_window.payload_controller:
            char_count, byte_count, line_count = self.main_window.payload_controller.get_payload_stats(payload)
            self.count_label.config(
                text=f"Chars: {char_count} | Bytes: {byte_count} | Lines: {line_count}"
            )

    def load_from_controller(self):
        """Load data from controller into UI."""
        # Load raw payload
        if self.raw_text:
            self.raw_text.delete("1.0", "end")
            self.raw_text.insert("1.0", self.main_window.controller.raw_payload)

        # Load GET parameters
        if hasattr(self.main_window.controller, 'get_params'):
            get_params = self.main_window.controller.get_params
            if isinstance(get_params, dict):
                self.get_path_var.set(get_params.get("path", "/"))

                # Clear existing rows
                for row_data in self.get_rows[:]:
                    self._remove_get_param(row_data["row"])

                # Add parameter rows
                params = get_params.get("params", {})
                if isinstance(params, dict):
                    for key, value in params.items():
                        self._add_get_param(key, value)

        # Load POST parameters
        if hasattr(self.main_window.controller, 'post_params'):
            post_params = self.main_window.controller.post_params
            if isinstance(post_params, dict):
                self.post_path_var.set(post_params.get("path", "/"))
                self.post_content_type_var.set(post_params.get("content_type", "application/x-www-form-urlencoded"))

                # Clear existing rows
                for row_data in self.post_rows[:]:
                    self._remove_post_param(row_data["row"])

                # Add parameter rows
                params = post_params.get("params", {})
                if isinstance(params, dict):
                    for key, value in params.items():
                        self._add_post_param(key, value)
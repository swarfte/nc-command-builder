"""Command preview panel for displaying generated netcat commands."""

import ttkbootstrap as ttk
from tkinter import Text
from controller.app_controller import AppController


class CommandPreview(ttk.LabelFrame):
    """Panel for command preview and execution options."""

    def __init__(self, parent, main_window):
        """Initialize command preview panel.

        Args:
            parent: Parent widget
            main_window: Main window reference
        """
        super().__init__(parent, text="Command Preview")
        self.main_window = main_window
        self._build_ui()

    def _build_ui(self):
        """Build command preview UI."""
        inner = ttk.Frame(self)
        inner.pack(fill="x", padx=8, pady=8)

        # Options row
        opts = ttk.Frame(inner)
        opts.pack(fill="x")

        ttk.Checkbutton(opts, text="Verbose (-v)", variable=self.main_window.var_verbose).pack(
            side="left", padx=4
        )
        ttk.Checkbutton(opts, text="No DNS (-n)", variable=self.main_window.var_no_dns).pack(
            side="left", padx=4
        )
        ttk.Checkbutton(opts, text="Keep listening (-k)", variable=self.main_window.var_keep_listen).pack(
            side="left", padx=4
        )
        ttk.Checkbutton(opts, text="Auto Content-Length", variable=self.main_window.var_auto_content_length).pack(
            side="left", padx=4
        )

        ttk.Label(opts, text="Timeout (-w):").pack(side="left", padx=(12, 0))
        ttk.Entry(opts, textvariable=self.main_window.var_timeout, width=5).pack(side="left", padx=2)

        ttk.Label(opts, text="Close delay (-q):").pack(side="left", padx=(12, 0))
        ttk.Entry(opts, textvariable=self.main_window.var_close_delay, width=5).pack(side="left", padx=2)

        ttk.Label(opts, text="Bind (-s):").pack(side="left", padx=(12, 0))
        ttk.Entry(opts, textvariable=self.main_window.var_local_bind, width=12).pack(side="left", padx=2)

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

    def update_preview(self):
        """Update command preview display."""
        # Get command from controller
        if self.main_window.command_controller:
            command = self.main_window.command_controller.get_command_preview()
        else:
            # Fallback if controller not set yet
            controller = AppController()
            controller.host = self.main_window.var_host.get()
            controller.port = self.main_window.var_port.get()
            controller.mode = self.main_window.var_mode.get()
            controller.protocol = self.main_window.var_protocol.get()
            controller.flavor = self.main_window.var_flavor.get()
            controller.payload_mode = self.main_window.var_payload_mode.get()
            controller.send_method = self.main_window.var_send_method.get()
            controller.verbose = self.main_window.var_verbose.get()
            controller.no_dns = self.main_window.var_no_dns.get()
            controller.timeout = self.main_window.var_timeout.get()
            controller.close_delay = self.main_window.var_close_delay.get()
            controller.keep_listen = self.main_window.var_keep_listen.get()
            controller.local_bind = self.main_window.var_local_bind.get()
            controller.auto_content_length = self.main_window.var_auto_content_length.get()
            command = controller.get_command()

        self.cmd_text.config(state="normal")
        self.cmd_text.delete("1.0", "end")
        self.cmd_text.insert("1.0", command)
        self.cmd_text.config(state="disabled")

    def _copy_command(self):
        """Copy command to clipboard."""
        if self.main_window.command_controller:
            # Use the main window's clipboard methods
            clipboard = self.main_window
            success = self.main_window.command_controller.copy_command_to_clipboard(clipboard)
            if success:
                self.main_window.flash_feedback("Command copied!")

    def _copy_payload(self):
        """Copy payload to clipboard."""
        if self.main_window.command_controller:
            # Use the main window's clipboard methods
            clipboard = self.main_window
            success = self.main_window.command_controller.copy_payload_to_clipboard(clipboard)
            if success:
                self.main_window.flash_feedback("Payload copied!")

    def _run_command(self):
        """Run command in terminal."""
        if self.main_window.command_controller:
            success = self.main_window.command_controller.run_command_in_terminal()
            if success:
                self.main_window.flash_feedback("Command launched!")
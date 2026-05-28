"""Target panel for host, port, mode, and protocol settings."""

import ttkbootstrap as ttk
from tkinter import StringVar
from model.nc_config import NC_FLAVORS


class TargetPanel(ttk.LabelFrame):
    """Panel for target and mode settings."""

    def __init__(self, parent, main_window):
        """Initialize target panel.

        Args:
            parent: Parent widget
            main_window: Main window reference
        """
        super().__init__(parent, text="Target & Mode")
        self.main_window = main_window
        self._build_ui()

    def _build_ui(self):
        """Build target panel UI."""
        inner = ttk.Frame(self)
        inner.pack(fill="x", padx=8, pady=8)

        # Host
        ttk.Label(inner, text="Host:").grid(row=0, column=0, sticky="w")
        ttk.Entry(inner, textvariable=self.main_window.var_host, width=24).grid(
            row=0, column=1, padx=4
        )

        # Port
        ttk.Label(inner, text="Port:").grid(row=0, column=2, sticky="w", padx=(8, 0))
        ttk.Entry(inner, textvariable=self.main_window.var_port, width=8).grid(
            row=0, column=3, padx=4
        )

        # Mode
        ttk.Label(inner, text="Mode:").grid(row=0, column=4, sticky="w", padx=(8, 0))
        ttk.Combobox(
            inner, textvariable=self.main_window.var_mode,
            values=["Connect", "Listen"], state="readonly", width=8,
        ).grid(row=0, column=5, padx=4)

        # Protocol
        ttk.Label(inner, text="Protocol:").grid(row=0, column=6, sticky="w", padx=(8, 0))
        ttk.Combobox(
            inner, textvariable=self.main_window.var_protocol,
            values=["TCP", "UDP"], state="readonly", width=5,
        ).grid(row=0, column=7, padx=4)

        # nc flavor
        ttk.Label(inner, text="nc flavor:").grid(row=0, column=8, sticky="w", padx=(8, 0))
        ttk.Combobox(
            inner, textvariable=self.main_window.var_flavor,
            values=list(NC_FLAVORS.keys()), state="readonly", width=14,
        ).grid(row=0, column=9, padx=4)
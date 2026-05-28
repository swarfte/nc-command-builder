"""Main application window for netcat command builder."""

import ttkbootstrap as ttk
from tkinter import StringVar, BooleanVar
import sys
from model.nc_config import RESOURCE_DIR


class MainWindow(ttk.Window):
    """Main application window with MVC architecture."""

    def __init__(self, controller):
        """Initialize main window.

        Args:
            controller: Application controller
        """
        super().__init__(themename="litera")
        self.title("Netcat Command Builder")
        self.geometry("960x720")
        self.minsize(800, 600)

        self.controller = controller
        self.payload_controller = None  # Will be set by main
        self.profile_controller = None  # Will be set by main
        self.command_controller = None  # Will be set by main

        # Initialize UI variables
        self._init_variables()

        # Set up window icon
        self._setup_icon()

        # Build UI components
        self._build_ui()

        # Update initial command preview
        self._update_preview()

    def _init_variables(self):
        """Initialize tkinter variables for UI binding."""
        # Target settings
        self.var_host = StringVar(value=self.controller.host)
        self.var_port = StringVar(value=self.controller.port)
        self.var_mode = StringVar(value=self.controller.mode)
        self.var_protocol = StringVar(value=self.controller.protocol)
        self.var_flavor = StringVar(value=self.controller.flavor)

        # Payload settings
        self.var_payload_mode = StringVar(value=self.controller.payload_mode)
        self.var_send_method = StringVar(value=self.controller.send_method)
        self.var_editor_mode = StringVar(value=self.controller.editor_mode)

        # Options
        self.var_verbose = BooleanVar(value=self.controller.verbose)
        self.var_no_dns = BooleanVar(value=self.controller.no_dns)
        self.var_timeout = StringVar(value=self.controller.timeout)
        self.var_close_delay = StringVar(value=self.controller.close_delay)
        self.var_keep_listen = BooleanVar(value=self.controller.keep_listen)
        self.var_local_bind = StringVar(value=self.controller.local_bind)
        self.var_auto_content_length = BooleanVar(value=self.controller.auto_content_length)

        # Trace updates for command preview
        self._setup_variable_traces()

    def _setup_variable_traces(self):
        """Set up variable traces for live command preview updates."""
        variables = [
            self.var_host, self.var_port, self.var_mode, self.var_protocol,
            self.var_flavor, self.var_payload_mode, self.var_send_method,
            self.var_verbose, self.var_no_dns, self.var_timeout,
            self.var_close_delay, self.var_keep_listen, self.var_local_bind,
            self.var_auto_content_length, self.var_editor_mode
        ]

        for var in variables:
            var.trace_add("write", lambda *_: self._update_preview())

    def _setup_icon(self):
        """Set up window icon."""
        # Window icon setup will be called by the main function
        # This is a placeholder for the icon setup logic
        pass

    def _build_ui(self):
        """Build main UI layout."""
        # Import view components here to avoid circular imports
        from view.sidebar import Sidebar
        from view.target_panel import TargetPanel
        from view.payload_editor import PayloadEditor
        from view.command_preview import CommandPreview

        # Create main layout with sidebar and content area
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True)

        # Configure grid weights
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(0, weight=1)

        # Left sidebar for profiles (resizable)
        self.sidebar = Sidebar(main_container, self)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 4), pady=8)

        # Right content area
        content_area = ttk.Frame(main_container)
        content_area.grid(row=0, column=1, sticky="nsew")
        content_area.columnconfigure(0, weight=1)
        content_area.rowconfigure(1, weight=1)

        # Target panel at top
        self.target_panel = TargetPanel(content_area, self)
        self.target_panel.pack(fill="x", padx=8, pady=(8, 4))

        # Payload editor in middle
        self.payload_editor = PayloadEditor(content_area, self)
        self.payload_editor.pack(fill="both", expand=True, padx=8, pady=4)

        # Command preview at bottom
        self.command_preview = CommandPreview(content_area, self)
        self.command_preview.pack(fill="x", padx=8, pady=(4, 8))

    def _update_preview(self):
        """Update command preview and sync variables with controller."""
        # Sync UI variables to controller
        self.controller.host = self.var_host.get()
        self.controller.port = self.var_port.get()
        self.controller.mode = self.var_mode.get()
        self.controller.protocol = self.var_protocol.get()
        self.controller.flavor = self.var_flavor.get()
        self.controller.payload_mode = self.var_payload_mode.get()
        self.controller.send_method = self.var_send_method.get()
        self.controller.verbose = self.var_verbose.get()
        self.controller.no_dns = self.var_no_dns.get()
        self.controller.timeout = self.var_timeout.get()
        self.controller.close_delay = self.var_close_delay.get()
        self.controller.keep_listen = self.var_keep_listen.get()
        self.controller.local_bind = self.var_local_bind.get()
        self.controller.auto_content_length = self.var_auto_content_length.get()
        self.controller.editor_mode = self.var_editor_mode.get()

        # Update command preview if it exists
        if hasattr(self, 'command_preview'):
            self.command_preview.update_preview()

        # Update payload stats if they exist
        if hasattr(self, 'payload_editor'):
            self.payload_editor.update_stats()

    def sync_from_controller(self):
        """Sync UI variables from controller state."""
        self.var_host.set(self.controller.host)
        self.var_port.set(self.controller.port)
        self.var_mode.set(self.controller.mode)
        self.var_protocol.set(self.controller.protocol)
        self.var_flavor.set(self.controller.flavor)
        self.var_payload_mode.set(self.controller.payload_mode)
        self.var_send_method.set(self.controller.send_method)
        self.var_verbose.set(self.controller.verbose)
        self.var_no_dns.set(self.controller.no_dns)
        self.var_timeout.set(self.controller.timeout)
        self.var_close_delay.set(self.controller.close_delay)
        self.var_keep_listen.set(self.controller.keep_listen)
        self.var_local_bind.set(self.controller.local_bind)
        self.var_auto_content_length.set(self.controller.auto_content_length)
        self.var_editor_mode.set(self.controller.editor_mode)

        # Update editor-specific data
        if hasattr(self, 'payload_editor'):
            self.payload_editor.load_from_controller()

    def flash_feedback(self, message: str):
        """Show temporary feedback message in window title.

        Args:
            message: Feedback message to display
        """
        old_title = self.title()
        self.title(f"{old_title}  —  {message}")
        self.after(1500, lambda: self.title(old_title))

    def set_controller_refs(self, payload_controller, profile_controller, command_controller):
        """Set controller references for UI components.

        Args:
            payload_controller: Payload controller instance
            profile_controller: Profile controller instance
            command_controller: Command controller instance
        """
        self.payload_controller = payload_controller
        self.profile_controller = profile_controller
        self.command_controller = command_controller
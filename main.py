"""Netcat Command Builder - MVC Architecture Entry Point."""

import sys
import ttkbootstrap as ttk
from pathlib import Path

# Import MVC components
from controller import AppController, PayloadController, ProfileController, CommandController
from view import MainWindow

# Setup application directories
APP_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
RESOURCE_DIR = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else APP_DIR


def setup_window_icon(window):
    """Set up window icon."""
    icon_dir = RESOURCE_DIR / "icons"
    if sys.platform == "win32":
        ico = icon_dir / "netcat-logo.ico"
        if ico.exists():
            window.iconbitmap(str(ico))
    png = icon_dir / "netcat-logo.png"
    if png.exists():
        window._icon_img = ttk.PhotoImage(file=str(png))
        window.iconphoto(True, window._icon_img)


def main():
    """Main entry point for the application."""
    # Initialize controllers
    app_controller = AppController()
    payload_controller = PayloadController(app_controller)
    profile_controller = ProfileController(app_controller)
    command_controller = CommandController(app_controller)

    # Initialize main window
    main_window = MainWindow(app_controller)

    # Set controller references
    main_window.set_controller_refs(payload_controller, profile_controller, command_controller)

    # Setup window icon
    setup_window_icon(main_window)

    # Start application
    main_window.mainloop()


if __name__ == "__main__":
    main()
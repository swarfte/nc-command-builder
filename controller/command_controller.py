"""Command controller for command generation and operations."""

class CommandController:
    """Controller for command generation and execution operations."""

    def __init__(self, app_controller):
        """Initialize command controller.

        Args:
            app_controller: Main application controller
        """
        self.app = app_controller

    def get_command_preview(self) -> str:
        """Get current command preview.

        Returns:
            Complete nc command string
        """
        return self.app.get_command()

    def copy_command_to_clipboard(self, window) -> bool:
        """Copy command to system clipboard.

        Args:
            window: Tkinter window with clipboard methods

        Returns:
            True if successful
        """
        try:
            command = self.get_command_preview()
            window.clipboard_clear()
            window.clipboard_append(command)
            return True
        except Exception:
            return False

    def copy_payload_to_clipboard(self, window) -> bool:
        """Copy current payload to clipboard.

        Args:
            window: Tkinter window with clipboard methods

        Returns:
            True if successful
        """
        try:
            payload = self.app._get_current_payload()
            window.clipboard_clear()
            window.clipboard_append(payload)
            return True
        except Exception:
            return False

    def run_command_in_terminal(self) -> bool:
        """Run command in new terminal window.

        Returns:
            True if command was launched successfully
        """
        try:
            import subprocess
            import platform

            cmd = self.get_command_preview()
            if not cmd:
                return False

            if platform.system() == "Windows":
                subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", cmd])
            else:
                subprocess.Popen(["x-terminal-emulator", "-e", "bash", "-c", cmd])
            return True
        except Exception:
            return False

    def validate_command(self) -> tuple:
        """Validate current command configuration.

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required fields
        if not self.app.host:
            return False, "Host is required"

        if not self.app.port:
            return False, "Port is required"

        # Validate port is numeric
        try:
            port_num = int(self.app.port)
            if port_num < 1 or port_num > 65535:
                return False, "Port must be between 1 and 65535"
        except ValueError:
            return False, "Port must be a valid number"

        # Check if mode requires payload
        if self.app.mode == "Connect" and not self.app._get_current_payload():
            # Empty payload is allowed for connect mode
            pass

        return True, ""

    def get_command_info(self) -> dict:
        """Get detailed information about the current command.

        Returns:
            Dictionary with command details
        """
        command = self.get_command_preview()
        payload = self.app._get_current_payload()

        return {
            "command": command,
            "payload_length": len(payload),
            "has_payload": bool(payload.strip()),
            "mode": self.app.mode,
            "protocol": self.app.protocol,
            "flavor": self.app.flavor,
            "target": f"{self.app.host}:{self.app.port}",
        }
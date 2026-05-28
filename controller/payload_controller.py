"""Payload controller for managing payload editing operations."""

from model.template_manager import TemplateManager
from model.payload_transformer import payload_to_printf


class PayloadController:
    """Controller for payload editing operations."""

    def __init__(self, app_controller):
        """Initialize payload controller.

        Args:
            app_controller: Main application controller
        """
        self.app = app_controller
        self.template_manager = TemplateManager()

    def get_template_names(self) -> list:
        """Get list of available template names.

        Returns:
            List of template names
        """
        return self.template_manager.get_all_template_names()

    def apply_template(self, name: str) -> tuple:
        """Apply template and return (payload, suggested_mode).

        Args:
            name: Template name

        Returns:
            Tuple of (payload_string, suggested_payload_mode)
        """
        payload = self.template_manager.apply_template(
            name,
            host=self.app.host,
            length=len("data=hello")  # Default length
        )

        # Get suggested mode for this template
        suggested_mode = self.template_manager.get_payload_mode_for_template(name)

        # Update raw payload with template
        self.app.raw_payload = payload.replace("\\r\\n", "\n")

        return payload, suggested_mode

    def process_payload_for_command(self, payload: str) -> str:
        """Process payload for command generation.

        Args:
            payload: Raw payload string

        Returns:
            Processed payload string
        """
        return payload_to_printf(
            payload,
            self.app.payload_mode,
            self.app.send_method
        )

    def get_payload_stats(self, payload: str) -> tuple:
        """Get payload character/byte/line statistics.

        Args:
            payload: Raw payload string

        Returns:
            Tuple of (char_count, byte_count, line_count)
        """
        char_count = len(payload)
        line_count = payload.count("\n") + 1 if payload else 0

        printf_str = payload_to_printf(
            payload,
            self.app.payload_mode,
            self.app.send_method
        )
        byte_count = len(printf_str.encode("utf-8", errors="replace"))

        return char_count, byte_count, line_count

    def url_encode_payload(self, payload: str) -> str:
        """URL-encode payload string.

        Args:
            payload: Raw payload string

        Returns:
            URL-encoded payload
        """
        import urllib.parse
        from utils.escape_handlers import interpret_escapes

        decoded = interpret_escapes(payload)
        return urllib.parse.quote(decoded, safe="")
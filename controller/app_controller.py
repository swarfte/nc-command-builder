"""Main application controller coordinating all components."""

from model.profile_manager import ProfileManager
from model.template_manager import TemplateManager
from model.command_builder import build_command


class AppController:
    """Main controller coordinating application logic."""

    def __init__(self):
        """Initialize application controller."""
        self.profile_manager = ProfileManager()
        self.template_manager = TemplateManager()

        # Application state
        self.current_profile = None
        self.editor_mode = "raw_tcp"  # raw_tcp, get, post

        # Target settings
        self.host = "127.0.0.1"
        self.port = "1337"
        self.mode = "Connect"
        self.protocol = "TCP"
        self.flavor = "GNU netcat"

        # Payload settings
        self.payload_mode = "Escapes (\\r\\n, \\x41)"
        self.send_method = "printf"

        # Options
        self.verbose = True
        self.no_dns = True
        self.timeout = "5"
        self.close_delay = ""
        self.keep_listen = True
        self.local_bind = ""
        self.auto_content_length = False

        # Independent mode data
        self.raw_payload = ""
        self.get_params = {}  # path: "", params: {key: value}
        self.post_params = {}  # content_type: "", params: {key: value}

    def get_command(self) -> str:
        """Generate command preview based on current state.

        Returns:
            Complete nc command string
        """
        # Get payload based on current editor mode
        payload = self._get_current_payload()

        # Apply auto content-length if enabled
        if self.auto_content_length and self.editor_mode == "post":
            payload = self._apply_auto_content_length(payload)

        return build_command(
            host=self.host,
            port=self.port,
            mode=self.mode,
            protocol=self.protocol,
            flavor=self.flavor,
            payload=payload,
            payload_mode=self.payload_mode,
            send_method=self.send_method,
            verbose=self.verbose,
            no_dns=self.no_dns,
            timeout=self.timeout,
            close_delay=self.close_delay,
            keep_listen=self.keep_listen,
            local_bind=self.local_bind,
        )

    def _get_current_payload(self) -> str:
        """Get payload based on current editor mode.

        Returns:
            Payload string for current mode
        """
        if self.editor_mode == "raw_tcp":
            return self.raw_payload
        elif self.editor_mode == "get":
            return self._build_get_payload()
        elif self.editor_mode == "post":
            return self._build_post_payload()
        return ""

    def _build_get_payload(self) -> str:
        """Build HTTP GET request from GET parameters.

        Returns:
            HTTP GET request string
        """
        path = self.get_params.get("path", "/")
        params = self.get_params.get("params", {})

        # Build query string
        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            path = f"{path}?{query_string}"

        return f"GET {path} HTTP/1.1\r\nHost: {self.host}\r\nConnection: close\r\n\r\n"

    def _build_post_payload(self) -> str:
        """Build HTTP POST request from POST parameters.

        Returns:
            HTTP POST request string
        """
        path = self.post_params.get("path", "/")
        content_type = self.post_params.get("content_type", "application/x-www-form-urlencoded")
        params = self.post_params.get("params", {})

        # Build body
        if params:
            if content_type == "application/x-www-form-urlencoded":
                body = "&".join(f"{k}={v}" for k, v in params.items())
            elif content_type == "application/json":
                import json
                body = json.dumps(params)
            else:
                body = "&".join(f"{k}={v}" for k, v in params.items())
        else:
            body = ""

        # Build headers
        headers = [
            f"POST {path} HTTP/1.1",
            f"Host: {self.host}",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(body.encode('utf-8', errors='surrogateescape'))}",
            "Connection: close",
            "",
            body
        ]

        return "\r\n".join(headers)

    def _apply_auto_content_length(self, payload: str) -> str:
        """Replace Content-Length header value with calculated body byte length.

        Args:
            payload: Original payload with potentially incorrect Content-Length

        Returns:
            Payload with corrected Content-Length
        """
        import re
        from utils.escape_handlers import interpret_escapes

        # Find blank line separating headers from body
        sep = "\r\n\r\n" if "\r\n\r\n" in payload else "\n\n"
        parts = payload.split(sep, 1)
        if len(parts) < 2:
            return payload  # No body found

        headers, body = parts

        # Calculate actual byte length of body
        if self.payload_mode == "Escapes (\\r\\n, \\x41)":
            body_bytes = len(interpret_escapes(body).encode("utf-8", errors="surrogateescape"))
        else:
            body_bytes = len(body.encode("utf-8", errors="surrogateescape"))

        # Replace Content-Length value in headers
        new_headers = re.sub(
            r"(Content-Length:\s*)\d+",
            rf"\g<1>{body_bytes}",
            headers,
            flags=re.IGNORECASE,
        )
        return new_headers + sep + body

    def update_editor_mode(self, mode: str):
        """Update current editor mode.

        Args:
            mode: One of 'raw_tcp', 'get', 'post'
        """
        self.editor_mode = mode

    def update_target_setting(self, key: str, value: str):
        """Update target connection settings.

        Args:
            key: Setting name (host, port, mode, protocol, flavor)
            value: New value
        """
        if hasattr(self, key):
            setattr(self, key, value)

    def update_payload_setting(self, key: str, value):
        """Update payload settings.

        Args:
            key: Setting name (payload_mode, send_method, raw_payload)
            value: New value
        """
        if key == "raw_payload":
            self.raw_payload = value
        elif hasattr(self, key):
            setattr(self, key, value)

    def update_option(self, key: str, value):
        """Update option settings.

        Args:
            key: Option name (verbose, no_dns, timeout, etc.)
            value: New value
        """
        if hasattr(self, key):
            setattr(self, key, value)

    def update_get_params(self, path: str = None, params: dict = None):
        """Update GET parameters.

        Args:
            path: Request path
            params: Dictionary of query parameters
        """
        if path is not None:
            self.get_params["path"] = path
        if params is not None:
            self.get_params["params"] = params

    def update_post_params(self, path: str = None, content_type: str = None, params: dict = None):
        """Update POST parameters.

        Args:
            path: Request path
            content_type: Content-Type header value
            params: Dictionary of body parameters
        """
        if path is not None:
            self.post_params["path"] = path
        if content_type is not None:
            self.post_params["content_type"] = content_type
        if params is not None:
            self.post_params["params"] = params

    def save_profile(self, name: str) -> str:
        """Save current state as profile.

        Args:
            name: Profile name

        Returns:
            Path to saved profile
        """
        profile_data = {
            "name": name,
            "folder": "Uncategorized",
            "editor_mode": self.editor_mode,
            "host": self.host,
            "port": self.port,
            "mode": self.mode,
            "protocol": self.protocol,
            "flavor": self.flavor,
            "payload_mode": self.payload_mode,
            "send_method": self.send_method,
            "verbose": self.verbose,
            "no_dns": self.no_dns,
            "timeout": self.timeout,
            "close_delay": self.close_delay,
            "keep_listen": self.keep_listen,
            "local_bind": self.local_bind,
            "auto_content_length": self.auto_content_length,
            # Mode-specific data
            "raw_payload": self.raw_payload,
            "get_params": self.get_params,
            "post_params": self.post_params,
        }

        return self.profile_manager.save_profile(name, profile_data)

    def load_profile(self, name: str) -> dict:
        """Load profile and update current state.

        Args:
            name: Profile name

        Returns:
            Profile data dictionary
        """
        profile_data = self.profile_manager.load_profile(name)

        # Update current state with profile data
        for key, value in profile_data.items():
            if key in ["get_params", "post_params"] and isinstance(value, dict):
                setattr(self, key, value)
            elif hasattr(self, key):
                setattr(self, key, value)

        self.current_profile = name
        return profile_data

    def delete_profile(self, name: str) -> bool:
        """Delete profile.

        Args:
            name: Profile name

        Returns:
            True if deleted successfully
        """
        return self.profile_manager.delete_profile(name)

    def list_profiles(self) -> list:
        """Get list of available profile names.

        Returns:
            List of profile names
        """
        return self.profile_manager.list_profiles()

    def get_all_profiles_data(self) -> dict:
        """Get all profile data.

        Returns:
            Dictionary mapping profile names to their data
        """
        return self.profile_manager.get_all_profile_data()
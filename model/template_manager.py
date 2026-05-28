"""Template management for payload templates."""

from model.nc_config import TEMPLATES


class TemplateManager:
    """Manages payload templates and template application."""

    def get_template(self, name: str) -> str:
        """Get template by name."""
        return TEMPLATES.get(name, "")

    def get_all_template_names(self) -> list:
        """Get list of all available template names."""
        return list(TEMPLATES.keys())

    def apply_template(self, name: str, host: str = "127.0.0.1", length: int = 9) -> str:
        """Apply template with variable substitution.

        Args:
            name: Template name
            host: Host address to substitute
            length: Content-Length value for POST templates

        Returns:
            Template string with variables substituted
        """
        template = self.get_template(name)
        if not template:
            return ""

        # Replace template variables
        template = template.replace("{host}", host).replace("{length}", str(length))
        return template

    def get_payload_mode_for_template(self, name: str) -> str:
        """Get appropriate payload mode for a template."""
        if "HTTP" in name or "SMTP" in name or "Redis" in name:
            return "Escapes (\\r\\n, \\x41)"
        return "Plain text"
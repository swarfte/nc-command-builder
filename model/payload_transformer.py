"""Payload transformation logic for different encoding modes."""

import re
from utils.escape_handlers import interpret_escapes, url_encode_uri, escape_for_single_quotes


def payload_to_printf(raw: str, mode: str, send_method: str = "printf") -> str:
    """Convert payload to a printf/echo-safe string based on mode.

    Plain text  → minimal escaping, output inside double quotes.
    Escapes     → URL-encode style, output inside single quotes.
    """
    if mode == "Plain text":
        # Minimal escaping — payload and preview should look the same.
        # Only escape characters that would break the shell double-quote string.
        return raw.replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$").replace("`", "\\`")

    elif mode == "Escapes (\\r\\n, \\x41)":
        # URL-encode the URI portion of HTTP request lines; keep
        # headers/body literal.  Output targets single-quoted
        # printf '...' (or echo -e '...').
        pct = "%%" if send_method == "printf" else "%"
        lines = raw.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        result_lines = []
        is_http = False

        for i, line in enumerate(lines):
            if i == 0:
                # Detect HTTP request line: METHOD URI HTTP/x.x
                # Greedy .* captures the full URI (which may contain spaces).
                m = re.match(r'^(\w+)\s+(.*)\s+(HTTP/\S+)$', line)
                if m:
                    is_http = True
                    method, uri, version = m.groups()
                    result_lines.append(
                        f'{method} {url_encode_uri(uri, pct)} {version}'
                    )
                else:
                    # Non-HTTP first line — escape for single-quote safety
                    result_lines.append(escape_for_single_quotes(line, pct))
            else:
                # Headers / body — keep literal, only escape ' and \
                result_lines.append(escape_for_single_quotes(line, pct))

        result = '\\r\\n'.join(result_lines)
        # HTTP requires headers to end with a blank line (\r\n\r\n).
        # Auto-append if the user didn't include one.
        if is_http:
            if not result.endswith('\\r\\n'):
                result += '\\r\\n'
            if not result.endswith('\\r\\n\\r\\n'):
                result += '\\r\\n'
        return result
    elif mode == "Hex (41 42 43)":
        hex_clean = raw.strip().replace(",", " ").split()
        parts = []
        for h in hex_clean:
            try:
                byte_val = int(h, 16)
                if byte_val < 32 or byte_val in (34, 92):
                    parts.append(f"\\x{byte_val:02x}")
                elif byte_val == 10:
                    parts.append("\\n")
                elif byte_val == 13:
                    parts.append("\\r")
                else:
                    parts.append(chr(byte_val))
            except ValueError:
                continue
        return "".join(parts)
    elif mode == "Base64 decode → send":
        import base64
        try:
            decoded = base64.b64decode(raw)
            return "".join(
                f"\\x{b:02x}" if b < 32 or b in (34, 92) else chr(b)
                for b in decoded
            )
        except Exception:
            return raw
    return raw
"""Text escaping and URL encoding utilities."""

from model.nc_config import _URL_SAFE


def interpret_escapes(text: str) -> str:
    """Convert escape sequences to actual characters.

    \\n → LF, \\r → CR, \\t → TAB, \\xNN → hex byte, \\0 → null,
    \\\\ → literal backslash.  Other \\X sequences kept as-is.
    """
    out = []
    i = 0
    while i < len(text):
        if text[i] == '\\' and i + 1 < len(text):
            nxt = text[i + 1]
            if nxt == 'n':
                out.append('\n'); i += 2
            elif nxt == 'r':
                out.append('\r'); i += 2
            elif nxt == 't':
                out.append('\t'); i += 2
            elif nxt == '0':
                out.append('\0'); i += 2
            elif nxt in ('x', 'X') and i + 3 < len(text):
                hx = text[i + 2:i + 4]
                try:
                    out.append(chr(int(hx, 16))); i += 4
                except ValueError:
                    out.append(text[i]); i += 1
            elif nxt == '\\':
                out.append('\\'); i += 2
            else:
                out.append(text[i]); i += 1
        else:
            out.append(text[i]); i += 1
    return ''.join(out)


def url_encode_uri(uri: str, pct: str) -> str:
    """URL-encode a URI using %%XX (printf) or %XX (echo -e) format.

    Escape sequences (\\n, \\r, \\t, \\xNN, \\0) are first converted
    to actual bytes so that \\n becomes %%0A (LF) instead of %%5Cn.
    """
    decoded = interpret_escapes(uri)
    return ''.join(
        f'{pct}{ord(ch):02X}' if ch not in _URL_SAFE else ch
        for ch in decoded
    )


def escape_for_single_quotes(line: str, pct: str) -> str:
    """Escape a line for use inside shell single quotes.

    Single-quoted strings can't contain literal '.  We encode it as
    {pct}27 (the URL-encoded form).  Backslashes are doubled so that
    printf/echo-e interpret \\ as a literal backslash.
    """
    return line.replace('\\', '\\\\').replace("'", f'{pct}27')
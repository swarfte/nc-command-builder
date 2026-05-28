"""Command building logic for netcat commands."""

from model.nc_config import NC_FLAVORS


def build_command(
    host: str,
    port: str,
    mode: str,
    protocol: str,
    flavor: str,
    payload: str,
    payload_mode: str,
    send_method: str,
    verbose: bool,
    no_dns: bool,
    timeout: str,
    close_delay: str,
    keep_listen: bool,
    local_bind: str,
) -> str:
    """Build the final nc command string."""
    parts = []
    is_listen = mode == "Listen"
    is_udp = protocol == "UDP"
    flavor_key = NC_FLAVORS.get(flavor, "openbsd")

    # ── payload pipeline prefix ──
    payload_prefix = ""
    if payload.strip() and not is_listen:
        from model.payload_transformer import payload_to_printf
        printf_str = payload_to_printf(payload, payload_mode, send_method)
        is_escapes = payload_mode == "Escapes (\\r\\n, \\x41)"
        quote = "'" if is_escapes else '"'
        if send_method == "printf":
            payload_prefix = f"printf {quote}{printf_str}{quote} | "
        else:
            payload_prefix = f"echo -e {quote}{printf_str}{quote} | "

    # ── nc binary ──
    nc_bin = "ncat" if flavor_key == "ncat" else "nc"

    # ── flags ──
    flags = []
    needs_p = False
    if is_listen:
        flags.append("-l")
        if flavor_key == "gnu":
            pass  # GNU nc: -l implies -p not needed on some versions
        else:
            needs_p = True
    if verbose:
        flags.append("-v")
    if no_dns and not is_listen:
        flags.append("-n")
    if is_udp:
        flags.append("-u")
    if timeout:
        flags.extend(["-w", timeout])
    if close_delay and flavor_key == "openbsd":
        flags.extend(["-q", close_delay])
    if close_delay and flavor_key == "ncat":
        flags.extend(["-q", close_delay])
    if local_bind and is_listen:
        flags.extend(["-s", local_bind])
    if keep_listen and is_listen:
        flags.append("-k")

    # ── host/port (ensure -p sits directly before port) ──
    target = []
    if is_listen:
        if needs_p:
            target.extend(["-p", port])
        else:
            target.append(port)
    else:
        target.extend([host, port])

    cmd = payload_prefix + nc_bin + " " + " ".join(flags) + " " + " ".join(target)
    return cmd.strip()
# Build (Portable / Single-file)

> PyInstaller can only build for the OS it runs on. Run the command that matches your current platform.

## Windows

```bash
uv run pyinstaller --icon=icons/netcat-logo.ico --onefile --windowed --name "nc-command-builder" main.py
```

Output: `dist/nc-command-builder.exe`

## macOS

```bash
uv run pyinstaller --icon=icons/netcat-logo.png --onefile --windowed --name "nc-command-builder" main.py
```

Output: `dist/nc-command-builder.app`

> Note: For best results on macOS, convert the `.png` to `.icns` first:
>
> ```bash
> mkdir icons/netcat-logo.iconset
> sips -z 16 16     icons/netcat-logo.png --out icons/netcat-logo.iconset/icon_16x16.png
> sips -z 32 32     icons/netcat-logo.png --out icons/netcat-logo.iconset/icon_16x16@2x.png
> sips -z 32 32     icons/netcat-logo.png --out icons/netcat-logo.iconset/icon_32x32.png
> sips -z 64 64     icons/netcat-logo.png --out icons/netcat-logo.iconset/icon_32x32@2x.png
> sips -z 128 128   icons/netcat-logo.png --out icons/netcat-logo.iconset/icon_128x128.png
> sips -z 256 256   icons/netcat-logo.png --out icons/netcat-logo.iconset/icon_128x128@2x.png
> sips -z 256 256   icons/netcat-logo.png --out icons/netcat-logo.iconset/icon_256x256.png
> sips -z 512 512   icons/netcat-logo.png --out icons/netcat-logo.iconset/icon_256x256@2x.png
> iconutil -c icns icons/netcat-logo.iconset
> ```
>
> Then use `--icon=icons/netcat-logo.icns`.

## Linux

```bash
uv run pyinstaller --onefile --windowed --name "nc-command-builder" main.py
```

Output: `dist/nc-command-builder`

> Linux ELF binaries do not embed icons. To add a desktop entry with icon, create a `.desktop` file separately.

---

## Install (system-wide)

After building, copy the output to a location on your `PATH`:

### Windows (run in elevated terminal)

```powershell
copy dist\nc-command-builder.exe C:\Windows\System32\
```

Or add the `dist/` folder to your user `PATH` via System Properties > Environment Variables.

### macOS / Linux

```bash
sudo cp dist/nc-command-builder /usr/local/bin/
```

Or install to user-local bin (no sudo needed):

```bash
mkdir -p ~/.local/bin
cp dist/nc-command-builder ~/.local/bin/
# Ensure ~/.local/bin is in your PATH (add to ~/.bashrc or ~/.zshrc)
```

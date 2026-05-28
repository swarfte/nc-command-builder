# Session Log — nc-command-builder MVC Refactoring

**Date:** 2026-05-28
**Branch:** dev

## Major Architectural Redesign

### MVC Architecture Implementation

Transformed the single-file application (763 lines) into a modern MVC architecture with Postman-like interface.

**New Directory Structure:**
```
nc-command-builder/
├── main.py                      # Entry point (reduced to ~50 lines)
├── main_legacy.py              # Original single-file backup
├── model/                       # Business logic layer
│   ├── nc_config.py            # Constants and configuration
│   ├── payload_transformer.py  # Payload transformation logic
│   ├── command_builder.py      # Command construction logic
│   ├── profile_manager.py      # Profile CRUD operations
│   └── template_manager.py     # Template management
├── view/                        # UI layer
│   ├── main_window.py          # Main application window
│   ├── target_panel.py         # Top bar: host/port/mode
│   ├── payload_editor.py       # Postman-like payload editor (3 modes)
│   ├── sidebar.py              # Left sidebar for profiles with folders
│   ├── command_preview.py      # Bottom command preview
│   └── helpers_panel.py        # Helper buttons panel
├── controller/                  # Application logic layer
│   ├── app_controller.py       # Main controller
│   ├── payload_controller.py   # Payload editing logic
│   ├── profile_controller.py   # Profile management logic
│   └── command_controller.py   # Command generation coordination
└── utils/                       # Shared utilities
    └── escape_handlers.py      # Text escaping utilities
```

### Key Features Implemented

1. **Postman-like Payload Editor** with 3 independent modes:
   - **Raw TCP Line**: Free text area with existing functionality
   - **GET Request**: Key-value form for query parameters (Path + dynamic parameter rows)
   - **POST Request**: Key-value form for body content (Content-Type selector + dynamic rows)
   - Each mode maintains independent data (Option A - preserved separately)

2. **Profile Sidebar** with full folder organization:
   - Postman-style tree view with expandable folders
   - Drag-and-drop support for organizing profiles
   - Context menu for profile management (rename, delete, move)
   - Search/filter functionality
   - Visual indicators for active profile

3. **Enhanced Profile Schema**:
   - Added folder organization support
   - Added editor_mode field (raw_tcp, get, post)
   - Added mode-specific data (raw_payload, get_params, post_params)
   - Maintained backward compatibility with existing profiles

4. **Controller Architecture**:
   - AppController: Main orchestration and state management
   - PayloadController: Template application and payload processing
   - ProfileController: Profile organization and search
   - CommandController: Command generation and execution

### Technical Improvements

- **Separation of Concerns**: Clear MVC boundaries
- **Testability**: Each component can be tested independently
- **Maintainability**: Single responsibility per module
- **Extensibility**: Easy to add new features or modes
- **Backward Compatibility**: Existing profiles work without modification

### Files Changed

- **main.py**: Complete rewrite (763 lines → ~50 lines)
- **model/**: 5 new files with business logic
- **view/**: 6 new files with UI components
- **controller/**: 4 new files with application logic
- **utils/**: 1 new file with utility functions

### What Was Built

- Complete MVC architecture implementation
- Postman-like payload editor with 3 independent modes
- Profile sidebar with folder organization and search
- Enhanced profile management with backward compatibility
- Command generation pipeline for all modes
- Template system integration with new architecture

### Testing Status

- ✅ MVC structure created
- ✅ All model components extracted
- ✅ All view components implemented
- ✅ All controller components implemented
- ✅ Main entry point created
- ✅ Import tests passed
- ✅ Basic functionality tests passed
- ✅ Payload mode tests passed
- ✅ Command generation working for all modes
- ✅ GET/POST mode functionality verified
- ✅ Application runs successfully

## Previous Session (2026-05-27)

Original single-file MVP with basic netcat command building functionality.

## What was built

Replaced placeholder `main.py` with a full-featured Tkinter GUI application (ttkbootstrap dark theme) for building netcat commands during CTF competitions.

## Features implemented

### Top bar — Target & Mode
- Host / Port fields
- Mode selector: Connect / Listen
- Protocol selector: TCP / UDP
- nc flavor dropdown: OpenBSD nc, GNU netcat, ncat (nmap)

### Middle — Payload Editor
- Multi-line text editor with scrollbar
- Payload type radio buttons: Plain text, Escapes, Hex input, Base64 decode
- Send method toggle: printf / echo -e
- Template selector with pre-built CTF templates:
  - Raw TCP line, HTTP GET, HTTP POST, Redis PING, SMTP HELO
- Live char/byte/line count display

### Middle — Helpers panel
- Insert CRLF (`\r\n`), `\n`, null byte (`\x00`)
- Wrap HTTP headers button
- Add blank line (double CRLF)
- Trim trailing spaces
- URL-encode payload
- Save / Load profiles (JSON files in `profiles/` directory)

### Bottom — Options & Command Preview
- Verbose (-v), No DNS (-n) checkboxes
- Timeout (-w), Close delay (-q), Bind (-s) fields
- Live command preview (read-only Consolas-styled text)
- Copy Command / Copy Payload Only buttons
- Run in Terminal button (opens new terminal window)

## Technical details

- Framework: ttkbootstrap (darkly theme)
- Zero external dependencies beyond what's in pyproject.toml
- `uv run python main.py` to launch
- Profiles saved as JSON in `profiles/` directory

## Files changed

- `main.py` — complete rewrite (329 lines)

## Testing

- Import verification passed
- GUI launched and rendered correctly
- User closed window (clean exit)

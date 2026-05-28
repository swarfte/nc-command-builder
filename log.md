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
│   └── command_preview.py      # Bottom command preview
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
- **view/**: 5 new files with UI components (helpers panel removed)
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

### Recent Updates

**Helpers Panel Removal (2026-05-29):**
- Removed `view/helpers_panel.py` (deemed unnecessary)
- Updated imports in `view/main_window.py` and `view/__init__.py`
- Removed helpers panel from main window layout
- Updated test suite to remove HelpersPanel imports
- Application now has cleaner, more focused interface
- All tests passing after removal

**Profile Sidebar Enhancement (2026-05-29):**
- Removed "New Profile" and "New Folder" buttons from sidebar
- Implemented right-click context menu system
- Right-click on empty space: Shows "New Profile" and "New Folder" options
- Right-click on folder: Shows folder management options + "New Profile"
- Right-click on profile: Shows profile management options
- Added default profile creation system (Postman-like)
- Creates "My First Profile" in "My Collection" folder if no profiles exist
- Cleaner interface with better UX consistency

**Window Size Adjustment (2026-05-29):**
- Main window geometry updated to 1280x900 (from 960x720)
- Provides more workspace for Postman-like interface
- Better suited for modern screen resolutions

**Profile Sidebar Folder Fix (2026-05-29):**
- Fixed bug where all profiles showed as "Uncategorized" regardless of folder assignment
- Root cause: `save_profile()` method hardcoded folder to "Uncategorized", overwriting any folder assignment
- Implemented proper folder tracking in AppController state:
  - Added `current_folder` attribute (default: "General")
  - Updated `save_profile()` to use `self.current_folder`
  - Updated `load_profile()` to restore folder from profile data
  - Added `set_folder()` method for explicit folder assignment
- Improved profile creation UX:
  - Right-click on empty space: Creates profile in "General" folder (no dialog)
  - Right-click on specific folder: Creates profile in that folder
  - Removed redundant folder dialog when creating from empty space
- Updated profile rename logic to preserve folder assignment
- Updated default profile creation to use "General" folder
- All existing "Uncategorized" profiles remain unchanged (backward compatibility)

**Empty Folder Display Fix (2026-05-29):**
- Fixed bug where newly created folders didn't appear in sidebar until they had profiles
- Root cause: Sidebar only showed folders that contained profiles (derived from profile data)
- Implemented folder tracking system:
  - Added `known_folders` list to AppController to track all folders, including empty ones
  - Added `create_folder()` method to create folders immediately
  - Added `get_known_folders()` method to retrieve all folders
  - Updated `set_folder()` to auto-add unknown folders to known list
  - Updated `load_profile()` to add profile's folder to known list if missing
- Updated `get_profiles_by_folder()` to show all known folders, even empty ones
- Updated `_new_folder_dialog()` to immediately create folder and refresh sidebar
- Folders now appear immediately after creation, with or without profiles
- Default folder "General" is always available

**Sidebar Empty on App Startup Fix (2026-05-29):**
- Fixed bug where sidebar appeared empty when reopening the app
- Root cause: Sidebar initialized before controllers were set, so `_refresh_profiles()` returned early
- Initialization sequence issue:
  1. MainWindow created with AppController
  2. MainWindow._build_ui() creates Sidebar
  3. Sidebar._refresh_profiles() called, but profile_controller is None
  4. Controllers set later via set_controller_refs()
- Fixed by adding sidebar refresh in set_controller_refs():
  - After profile_controller is set, trigger sidebar._refresh_profiles()
  - This ensures existing profiles are displayed on app startup
- Added `_load_existing_folders()` to AppController.__init__():
  - Scans all existing profiles on startup
  - Populates known_folders with folders from existing profiles
  - Ensures folders are preserved across app sessions
- All existing profiles and folders now display correctly when app is reopened

**Auto-Save on Profile Switch (2026-05-29):**
- Added auto-save functionality when switching between profiles
- Prevents data loss when user loads a different profile
- Updated `_load_selected_profile()` in Sidebar:
  - Checks if there's a current_profile before loading new one
  - If yes, syncs UI state and saves current profile silently (no dialog)
  - Then loads the new profile
  - Shows feedback message indicating both save and load operations
- Updated `save_profile()` in AppController:
  - Now sets `current_profile` when saving (was missing before)
  - Ensures profile tracking works correctly throughout session
- Profile switching flow:
  1. User makes changes to current profile settings
  2. User double-clicks different profile in sidebar
  3. Current profile is auto-saved with all changes
  4. New profile is loaded
  5. Feedback shows: "Saved 'X' → Loaded 'Y'!"
- No more lost data when switching profiles!
- Auto-save is silent and doesn't require user confirmation

**Template and Settings Enhancements (2026-05-29):**
- Updated GET template: Changed from "GET /?flag=pwn HTTP/1.1" to "GET / HTTP/1.1"
- Added template tracking to AppController: New `template` attribute (default: "Custom")
- Updated save_profile() to include template selection in saved profile data
- Updated load_profile() to restore template selection when loading profiles
- Added template syncing in PayloadEditor:
  - _on_template() now updates controller with selected template
  - load_from_controller() now restores template selection from controller
- Added Ctrl+S keyboard shortcut for saving profiles:
  - Press Ctrl+S to save current profile with all settings
  - If no current profile, shows "Save Profile" dialog
  - Provides visual feedback when save is successful
- Enhanced profile persistence: All settings now saved and restored:
  - Target settings: host, port, mode, protocol, nc flavor
  - Payload settings: payload mode, send method, template selection
  - Options: verbose, no DNS, timeout, close delay, keep listen, local bind, auto content length
  - Mode-specific data: raw payload, GET parameters, POST parameters
  - Editor mode: raw_tcp, get, post
  - Folder assignment
- Profiles now maintain complete state across sessions
- When switching profiles or reopening app, user sees exact same configuration

**Critical Profile Switching Bug Fix (2026-05-29):**
- Fixed critical bug where all profiles appeared to have the same content when switching
- Root cause: `_load_selected_profile()` was calling `_update_preview()` after `sync_from_controller()`
- This caused newly loaded profile data to be overwritten with old UI state
- Incorrect flow:
  1. Load profile B into controller
  2. Sync UI from controller (UI now shows profile B)
  3. Call `_update_preview()` which syncs UI variables TO controller
  4. Controller state overwritten with old UI data
  5. All profiles end up with the same content
- Fixed flow:
  1. Auto-save current profile (if any) with current UI state
  2. Load new profile into controller
  3. Sync UI from controller (UI shows loaded profile)
  4. Update command preview only (no sync back to controller)
- Updated `_load_selected_profile()` method:
  - Removed problematic `_update_preview()` call after `sync_from_controller()`
  - Added specific command preview update instead
  - Ensures proper data flow: profile → controller → UI
- Profiles now maintain their unique data when switching
- Each profile correctly displays its own saved settings
- No more data corruption when switching between profiles

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

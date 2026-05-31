MVC Architecture and Postman-like Interface Implementation Plan
 Context

 Transform the current single-file netcat command builder (763 lines) into a modern MVC architecture with a Postman-like interface. The current application has
  clear separation concerns that can be extracted:

- Model Layer: Payload transformation logic (lines 113-187), command building (lines 190-263)
- View Layer: GUI code (lines 268-754)
- Controller Layer: Currently embedded in GUI class, needs extraction

 User Requirements:

1. MVC architecture from single-file design
2. Postman-like payload interface with 3 independent modes
3. Left sidebar for profile management with folder organization
4. Better UX similar to Postman/Apifox

 Recommended Approach

 Phase 1: Create MVC Skeleton (1-2 hours)

 Directory Structure:
 nc-command-builder/
 ├── main.py                      # Entry point (reduced to ~20 lines)
 ├── model/                       # Business logic layer
 │   ├── __init__.py
 │   ├── payload_transformer.py  # Payload transformation logic
 │   ├── command_builder.py       # Command construction logic
 │   ├── profile_manager.py      # Profile CRUD operations
 │   ├── template_manager.py      # Template management
 │   └── nc_config.py            # NC flavors, constants
 ├── view/                        # UI layer
 │   ├── __init__.py
 │   ├── main_window.py          # Main application window
 │   ├── target_panel.py         # Top bar: host/port/mode
 │   ├── payload_editor.py       # Postman-like payload editor (3 modes)
 │   ├── sidebar.py              # Left sidebar for profiles with folders
 │   ├── command_preview.py      # Bottom command preview
 │   └── helpers_panel.py        # Helper buttons panel
 ├── controller/                  # Application logic layer
 │   ├── __init__.py
 │   ├── app_controller.py       # Main controller
 │   ├── payload_controller.py   # Payload editing logic
 │   ├── profile_controller.py   # Profile management logic
 │   └── command_controller.py   # Command generation coordination
 ├── utils/                       # Shared utilities
 │   ├── __init__.py
 │   ├── escape_handlers.py      # Text escaping utilities
 │   └── validators.py           # Input validation
 └── profiles/                    # User profile JSON files (unchanged)

 Phase 2: Extract Model Layer (2-3 hours)

 Files to Create:

1. model/nc_config.py: Extract constants (lines 21-41)

- TEMPLATES, NC_FLAVORS, _URL_SAFE constants
- Application directory paths

2. utils/escape_handlers.py: Extract helper functions (lines 56-111)

- _interpret_escapes(): Convert escape sequences to actual characters
- _url_encode_uri(): URL-encode with escape sequence handling
- _escape_for_single_quotes(): Shell escaping for single quotes

3. model/payload_transformer.py: Extract payload transformation (lines 113-187)

- payload_to_printf(): Main payload transformation logic
- Import from utils.escape_handlers
- Preserve all 4 modes: Plain text, Escapes, Hex, Base64

4. model/command_builder.py: Extract command building (lines 190-263)

- build_command(): Assemble final nc command string
- Handle flavor-specific behavior and flag ordering

5. model/profile_manager.py: Extract profile operations (lines 674-754)

- save_profile(): Save profile data to JSON
- load_profile(): Load profile from JSON
- delete_profile(): Delete profile file
- list_profiles(): List all available profiles
- Maintain backward compatibility with existing JSON format

6. model/template_manager.py: Extract template logic (lines 536-549)

- get_template(): Retrieve template by name
- apply_template(): Apply template with variable substitution

 Phase 3: Create View Layer (3-4 hours)

 Key Design Decisions:

 Postman-like Payload Editor (view/payload_editor.py):

- 3 Independent Modes (Option A - data preserved separately per mode):
  a. Raw TCP Line: ScrolledText widget with existing functionality
  b. GET Request: Key-value form for query parameters (Path + dynamic parameter rows)
  c. POST Request: Key-value form for body content (Content-Type selector + dynamic rows)
- Mode Switching: Tab/radio button interface, each mode maintains independent data
- Auto Content-Length: Only active in POST mode, calculates body byte length

 Profile Sidebar (view/sidebar.py):

- Postman-style Folder Organization:
  - Tree view with expandable folders/collections
  - Drag-and-drop support for moving profiles between folders
  - Context menu: New Folder, Rename, Delete, Export Profile
  - Visual indicators for active profile
  - Search/filter profiles by name
- Quick Actions: Double-click to load, right-click for management

 Main Window (view/main_window.py):

- 3-Panel Layout:
  - Left: Profile sidebar (250px width, resizable)
  - Center: Main content (target panel + payload editor + helpers)
  - Bottom: Command preview (fixed height)
- Responsive Design: Panels resize with window

 Phase 4: Create Controller Layer (2-3 hours)

 Controllers to Create:

1. controller/app_controller.py: Main orchestration

- Initialize all components
- Handle startup/shutdown
- Coordinate between views and models

2. controller/payload_controller.py: Payload mode management

- Handle mode switching between Raw/GET/POST
- Maintain independent state for each mode
- Coordinate form data → payload generation
- Trigger command preview updates

3. controller/profile_controller.py: Profile management

- Handle sidebar interactions
- Coordinate profile CRUD operations
- Manage folder organization
- Handle profile switching

4. controller/command_controller.py: Command generation

- Coordinate payload transformation
- Generate command preview
- Handle copy/run operations

 Phase 5: Wire Everything Together (2-3 hours)

 Integration Steps:

1. Update main.py to simple entry point:
   from controller.app_controller import AppController
   from view.main_window import MainWindow

 def main():
     controller = AppController()
     window = MainWindow(controller)
     window.mainloop()
 2. Connect Data Flow:

- User Action → View Event → Controller → Model → Controller → View Update
- Example: Adding GET parameter triggers on_add_parameter() → controller updates form → model rebuilds query string → controller updates command preview →
  view refreshes

3. Implement Mode Switching:

- Each mode (Raw/GET/POST) has independent state
- Switching preserves each mode's data
- Command generation adapts to current mode

 Phase 6: Enhanced Profile Schema (1-2 hours)

 Extended Profile Format (maintaining backward compatibility):
 {
   "name": "HTTP GET Example",
   "folder": "CTF Challenges",
   "editor_mode": "get",
   "raw_payload": "",
   "get_params": {"path": "/challenge", "flag": "pwn"},
   "post_params": {},
   "content_type": "application/x-www-form-urlencoded",
   "host": "127.0.0.1",
   "port": "1337",
   "mode": "Connect",
   "protocol": "TCP",
   "flavor": "GNU netcat",
   "payload_mode": "Escapes (\\r\\n, \\x41)",
   "send_method": "printf",
   "verbose": true,
   "no_dns": true,
   "timeout": "5",
   "close_delay": "",
   "keep_listen": true,
   "local_bind": "",
   "auto_content_length": false
 }

 Migration Strategy:

- Old profiles load with default values for new fields
- New fields optional, default to sensible values
- Folder defaults to "Uncategorized" if not specified
- Editor mode defaults to "raw_tcp" if not specified

 Phase 7: Testing and Refinement (3-4 hours)

 Testing Strategy:

1. Regression Testing:

- Compare command output with original for all existing features
- Test profile backward compatibility
- Verify all helper buttons work identically

2. New Feature Testing:

- GET mode: Generate valid HTTP GET requests from key-value forms
- POST mode: Generate valid HTTP POST with correct Content-Length
- Profile sidebar: Create folders, organize profiles, quick switching

3. Integration Testing:

- Test data flow between MVC layers
- Test mode switching preserves independent data
- Test profile save/load with folder organization

4. Performance Testing:

- Ensure no performance degradation
- Test with large number of profiles
- Test responsiveness of UI updates

 Critical Files to Reference

- C:\Users\swarfte\Desktop\Coding\nc-command-builder\main.py (lines 1-763): Current single-file implementation
- C:\Users\swarfte\Desktop\Coding\nc-command-builder\model\payload_transformer.py: Will contain payload transformation logic (lines 113-187 from main.py)
- C:\Users\swarfte\Desktop\Coding\nc-command-builder\view\payload_editor.py: New 3-mode Postman-like payload editor
- C:\Users\swarfte\Desktop\Coding\nc-command-builder\view\sidebar.py: New Postman-style profile sidebar with folders

 Backward Compatibility Guarantees

- Profile Format: Add new fields as optional with sensible defaults
- Command Output: Maintain identical command generation for all existing features
- Feature Parity: Preserve all existing functionality (templates, helpers, options)
- Rollback Plan: Keep original main.py as main_legacy.py during migration

 Success Criteria

 Functional Requirements:

- ✅ All existing features work identically to original
- ✅ GET mode generates valid HTTP GET requests from key-value forms
- ✅ POST mode generates valid HTTP POST with correct Content-Length
- ✅ Profile sidebar with folder organization works fully
- ✅ Mode switching preserves independent data for each mode
- ✅ Real-time command preview works in all modes

 Non-Functional Requirements:

- ✅ Code organized in clear MVC structure
- ✅ Each module has single responsibility
- ✅ Backward compatibility with existing profiles
- ✅ No performance degradation
- ✅ Code is testable and maintainable

 Verification Steps

1. Run the application: uv run python main.py
2. Test existing features: Verify all original functionality works
3. Test new features: Try GET/POST modes, profile sidebar
4. Test profile compatibility: Load existing profiles, create new ones
5. Compare command output: Generate commands in both old and new versions for comparison
6. Performance check: Test with many profiles, large payloads
7. UI responsiveness: Ensure smooth transitions between modes

 Estimated Timeline

- Phase 1-2: MVC Skeleton and Model Extraction: 3-4 hours
- Phase 3: View Layer Creation: 3-4 hours
- Phase 4: Controller Implementation: 2-3 hours
- Phase 5: Integration: 2-3 hours
- Phase 6: Enhanced Profile Schema: 1-2 hours
- Phase 7: Testing and Refinement: 3-4 hours

 Total Estimated Time: 17-23 hours of focused development work

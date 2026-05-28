"""Sidebar for profile management with Postman-like folder organization."""

import ttkbootstrap as ttk
from tkinter import simpledialog, messagebox


class Sidebar(ttk.LabelFrame):
    """Sidebar for profile management with folder organization."""

    def __init__(self, parent, main_window):
        """Initialize sidebar.

        Args:
            parent: Parent widget
            main_window: Main window reference
        """
        super().__init__(parent, text="Profiles")
        self.main_window = main_window
        self._build_ui()

    def _build_ui(self):
        """Build sidebar UI."""
        inner = ttk.Frame(self)
        inner.pack(fill="both", expand=True, padx=8, pady=8)

        # Search bar
        search_frame = ttk.Frame(inner)
        search_frame.pack(fill="x", pady=(0, 4))

        self.search_var = ttk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(fill="x")
        search_entry.bind("<KeyRelease>", lambda e: self._filter_profiles())

        # Profile list
        self.profile_list = ttk.Treeview(inner, columns=("name",), show="tree headings", selectmode="browse")
        self.profile_list.heading("#0", text="Profiles", anchor="w")
        self.profile_list.column("name", width=200, anchor="w")
        self.profile_list.pack(fill="both", expand=True)

        # Bind double-click to load profile
        self.profile_list.bind("<Double-1>", lambda e: self._load_selected_profile())

        # Bind right-click for context menu
        self.profile_list.bind("<Button-3>", self._show_context_menu)

        # Management buttons
        btn_frame = ttk.Frame(inner)
        btn_frame.pack(fill="x", pady=(4, 0))

        ttk.Button(btn_frame, text="New Profile", command=self._save_profile_dialog, width=20, bootstyle="success").pack(
            pady=2, fill="x"
        )
        ttk.Button(btn_frame, text="New Folder", command=self._new_folder_dialog, width=20).pack(
            pady=2, fill="x"
        )

        # Initial load
        self._refresh_profiles()

    def _refresh_profiles(self):
        """Refresh profile list from controller."""
        # Clear existing items
        for item in self.profile_list.get_children():
            self.profile_list.delete(item)

        if not self.main_window.profile_controller:
            return

        # Get profiles by folder
        folders = self.main_window.profile_controller.get_profiles_by_folder()

        # Add folders and profiles
        for folder_name, profiles in folders.items():
            # Add folder node
            folder_id = self.profile_list.insert("", "end", text=folder_name, open=True)

            # Add profiles under folder
            for profile_name in profiles:
                self.profile_list.insert(folder_id, "end", text=profile_name, values=(profile_name,))

    def _filter_profiles(self):
        """Filter profiles based on search query."""
        search_query = self.search_var.get().lower()
        if not search_query:
            self._refresh_profiles()
            return

        # Clear existing items
        for item in self.profile_list.get_children():
            self.profile_list.delete(item)

        if not self.main_window.profile_controller:
            return

        # Search profiles
        matching_profiles = self.main_window.profile_controller.search_profiles(search_query)

        # Display matching profiles
        if matching_profiles:
            results_id = self.profile_list.insert("", "end", text="Search Results", open=True)
            for profile_name in matching_profiles:
                self.profile_list.insert(results_id, "end", text=profile_name, values=(profile_name,))

    def _load_selected_profile(self):
        """Load selected profile."""
        selection = self.profile_list.selection()
        if not selection:
            return

        item = selection[0]
        item_text = self.profile_list.item(item, "text")

        # Skip folders
        if self.profile_list.parent(item) == "":
            return

        # Get profile name
        profile_name = item_text

        # Load profile
        if self.main_window.profile_controller:
            try:
                self.main_window.controller.load_profile(profile_name)
                self.main_window.sync_from_controller()
                self.main_window._update_preview()
                self.main_window.flash_feedback(f"Profile '{profile_name}' loaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load profile: {e}")

    def _save_profile_dialog(self):
        """Show dialog to save new profile."""
        profile_name = simpledialog.askstring("Save Profile", "Profile name:", parent=self)
        if not profile_name:
            return

        # Ask for folder
        folder_name = simpledialog.askstring("Save Profile", "Folder name (leave empty for 'Uncategorized'):", parent=self)
        if not folder_name:
            folder_name = "Uncategorized"

        try:
            # Set folder in controller
            self.main_window.controller.save_profile(profile_name)
            # Update folder in profile
            self.main_window.profile_controller.rename_profile_folder(profile_name, folder_name)

            self._refresh_profiles()
            self.main_window.flash_feedback(f"Profile '{profile_name}' saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save profile: {e}")

    def _new_folder_dialog(self):
        """Show dialog to create new folder."""
        folder_name = simpledialog.askstring("New Folder", "Folder name:", parent=self)
        if not folder_name:
            return

        # Folders are created when profiles reference them
        self.main_window.flash_feedback(f"Folder '{folder_name}' created (add profiles to see it)")

    def _show_context_menu(self, event):
        """Show context menu for profile management."""
        selection = self.profile_list.selection()
        if not selection:
            return

        item = selection[0]
        item_text = self.profile_list.item(item, "text")

        # Create context menu
        context_menu = ttk.Menu(self, tearoff=0)

        if self.profile_list.parent(item) == "":
            # Folder menu
            context_menu.add_command(label="Rename Folder", command=lambda: self._rename_folder_dialog(item_text))
            context_menu.add_command(label="Delete Folder", command=lambda: self._delete_folder(item_text))
        else:
            # Profile menu
            context_menu.add_command(label="Load Profile", command=self._load_selected_profile)
            context_menu.add_separator()
            context_menu.add_command(label="Rename Profile", command=lambda: self._rename_profile_dialog(item_text))
            context_menu.add_command(label="Delete Profile", command=lambda: self._delete_profile(item_text))
            context_menu.add_separator()
            context_menu.add_command(label="Move to Folder", command=lambda: self._move_profile_dialog(item_text))

        # Show menu at cursor position
        context_menu.post(event.x_root, event.y_root)

    def _rename_folder_dialog(self, folder_name):
        """Show dialog to rename folder."""
        new_name = simpledialog.askstring("Rename Folder", "New folder name:", initialvalue=folder_name, parent=self)
        if not new_name or new_name == folder_name:
            return

        # Update all profiles in this folder
        if self.main_window.profile_controller:
            try:
                # Get profiles in folder
                folders = self.main_window.profile_controller.get_profiles_by_folder()
                profiles_in_folder = folders.get(folder_name, [])

                # Move each profile to new folder
                for profile_name in profiles_in_folder:
                    self.main_window.profile_controller.rename_profile_folder(profile_name, new_name)

                self._refresh_profiles()
                self.main_window.flash_feedback(f"Folder renamed to '{new_name}'!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename folder: {e}")

    def _delete_folder(self, folder_name):
        """Delete folder and its profiles."""
        confirm = messagebox.askyesno(
            "Delete Folder", f"Delete folder '{folder_name}' and all its profiles?", parent=self,
        )
        if not confirm:
            return

        if self.main_window.profile_controller:
            try:
                # Get profiles in folder
                folders = self.main_window.profile_controller.get_profiles_by_folder()
                profiles_in_folder = folders.get(folder_name, [])

                # Delete each profile
                for profile_name in profiles_in_folder:
                    self.main_window.controller.delete_profile(profile_name)

                self._refresh_profiles()
                self.main_window.flash_feedback(f"Folder '{folder_name}' deleted!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete folder: {e}")

    def _rename_profile_dialog(self, profile_name):
        """Show dialog to rename profile."""
        new_name = simpledialog.askstring("Rename Profile", "New profile name:", initialvalue=profile_name, parent=self)
        if not new_name or new_name == profile_name:
            return

        if self.main_window.profile_controller:
            try:
                # Load profile data
                profile_data = self.main_window.controller.load_profile(profile_name)

                # Save with new name
                self.main_window.controller.save_profile(new_name)
                self.main_window.profile_controller.rename_profile_folder(new_name, profile_data.get("folder", "Uncategorized"))

                # Delete old profile
                self.main_window.controller.delete_profile(profile_name)

                self._refresh_profiles()
                self.main_window.flash_feedback(f"Profile renamed to '{new_name}'!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename profile: {e}")

    def _delete_profile(self, profile_name):
        """Delete profile with confirmation."""
        confirm = messagebox.askyesno(
            "Delete Profile", f"Delete profile '{profile_name}'?", parent=self,
        )
        if not confirm:
            return

        if self.main_window.profile_controller:
            try:
                success = self.main_window.controller.delete_profile(profile_name)
                if success:
                    self._refresh_profiles()
                    self.main_window.flash_feedback(f"Profile '{profile_name}' deleted!")
                else:
                    messagebox.showerror("Error", f"Profile '{profile_name}' not found")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete profile: {e}")

    def _move_profile_dialog(self, profile_name):
        """Show dialog to move profile to different folder."""
        new_folder = simpledialog.askstring("Move Profile", "New folder name:", parent=self)
        if not new_folder:
            return

        if self.main_window.profile_controller:
            try:
                success = self.main_window.profile_controller.rename_profile_folder(profile_name, new_folder)
                if success:
                    self._refresh_profiles()
                    self.main_window.flash_feedback(f"Profile moved to '{new_folder}'!")
                else:
                    messagebox.showerror("Error", f"Failed to move profile")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to move profile: {e}")
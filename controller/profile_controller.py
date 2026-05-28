"""Profile controller for managing profile operations."""

class ProfileController:
    """Controller for profile management operations."""

    def __init__(self, app_controller):
        """Initialize profile controller.

        Args:
            app_controller: Main application controller
        """
        self.app = app_controller

    def get_profiles_by_folder(self) -> dict:
        """Get profiles organized by folder.

        Returns:
            Dictionary mapping folder names to lists of profile names
        """
        profiles_data = self.app.get_all_profiles_data()
        folders = {}

        # Initialize with all known folders (including empty ones)
        for folder in self.app.get_known_folders():
            folders[folder] = []

        # Add profiles to their folders
        for name, data in profiles_data.items():
            folder = data.get("folder", "General")
            if folder not in folders:
                # Folder exists in profile but not in known folders - add it
                folders[folder] = []
            folders[folder].append(name)

        return folders

    def create_folder(self, folder_name: str):
        """Create a new folder (logical organization).

        Args:
            folder_name: Name of the folder to create
        """
        # Folders are virtual - they exist when profiles reference them
        pass

    def rename_profile_folder(self, profile_name: str, new_folder: str) -> bool:
        """Change profile's folder assignment.

        Args:
            profile_name: Name of the profile to move
            new_folder: New folder name

        Returns:
            True if successful
        """
        try:
            profile_data = self.app.load_profile(profile_name)
            profile_data["folder"] = new_folder
            self.app.save_profile(profile_name)
            return True
        except Exception:
            return False

    def get_profile_info(self, profile_name: str) -> dict:
        """Get profile information.

        Args:
            profile_name: Name of the profile

        Returns:
            Profile data dictionary
        """
        try:
            return self.app.load_profile(profile_name)
        except Exception:
            return None

    def export_profile(self, profile_name: str, export_path: str) -> bool:
        """Export profile to external file.

        Args:
            profile_name: Name of the profile to export
            export_path: Path to export the profile to

        Returns:
            True if successful
        """
        try:
            import shutil
            profile_path = self.app.profile_manager.profiles_dir / f"{profile_name}.json"
            shutil.copy(profile_path, export_path)
            return True
        except Exception:
            return False

    def import_profile(self, import_path: str, new_name: str = None) -> bool:
        """Import profile from external file.

        Args:
            import_path: Path to import the profile from
            new_name: Optional new name for the imported profile

        Returns:
            True if successful
        """
        try:
            import shutil
            import json

            # Load the profile to check its name
            with open(import_path) as f:
                profile_data = json.load(f)

            profile_name = new_name or profile_data.get("name", "imported_profile")
            dest_path = self.app.profile_manager.profiles_dir / f"{profile_name}.json"
            shutil.copy(import_path, dest_path)
            return True
        except Exception:
            return False

    def search_profiles(self, query: str) -> list:
        """Search profiles by name or content.

        Args:
            query: Search query string

        Returns:
            List of matching profile names
        """
        matching_profiles = []
        profiles_data = self.app.get_all_profiles_data()

        query_lower = query.lower()
        for name, data in profiles_data.items():
            # Search in profile name
            if query_lower in name.lower():
                matching_profiles.append(name)
                continue

            # Search in folder name
            folder = data.get("folder", "")
            if query_lower in folder.lower():
                matching_profiles.append(name)
                continue

            # Search in host
            host = data.get("host", "")
            if query_lower in host.lower():
                matching_profiles.append(name)

        return matching_profiles
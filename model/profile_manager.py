"""Profile management for saving and loading netcat configurations."""

import json
import os
from pathlib import Path
from model.nc_config import PROFILES_DIR


class ProfileManager:
    """Manages profile CRUD operations."""

    def __init__(self):
        """Initialize profile manager."""
        self.profiles_dir = PROFILES_DIR
        self.profiles_dir.mkdir(exist_ok=True)

    def save_profile(self, name: str, data: dict) -> str:
        """Save profile data to JSON file.

        Args:
            name: Profile name (without .json extension)
            data: Profile data dictionary

        Returns:
            Path to saved profile file
        """
        path = self.profiles_dir / f"{name}.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        return str(path)

    def load_profile(self, name: str) -> dict:
        """Load profile data from JSON file.

        Args:
            name: Profile name (without .json extension)

        Returns:
            Profile data dictionary
        """
        path = self.profiles_dir / f"{name}.json"
        with open(path) as f:
            return json.load(f)

    def delete_profile(self, name: str) -> bool:
        """Delete profile file.

        Args:
            name: Profile name (without .json extension)

        Returns:
            True if deleted, False if not found
        """
        path = self.profiles_dir / f"{name}.json"
        if path.exists():
            path.unlink()
            return True
        return False

    def list_profiles(self) -> list:
        """List all available profile names.

        Returns:
            List of profile names (without .json extension)
        """
        if not self.profiles_dir.exists():
            return []

        files = list(self.profiles_dir.glob("*.json"))
        return [f.stem for f in files]

    def profile_exists(self, name: str) -> bool:
        """Check if profile exists.

        Args:
            name: Profile name (without .json extension)

        Returns:
            True if profile exists
        """
        path = self.profiles_dir / f"{name}.json"
        return path.exists()

    def get_all_profile_data(self) -> dict:
        """Get all profile data with metadata.

        Returns:
            Dictionary mapping profile names to their data
        """
        profiles = {}
        for name in self.list_profiles():
            try:
                profiles[name] = self.load_profile(name)
            except Exception:
                # Skip corrupted profiles
                continue
        return profiles
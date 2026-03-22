"""Registration module for Street Race Manager."""


class RegistrationModule:
    """Stores crew members and their assigned roles."""

    VALID_ROLES = {"driver", "mechanic", "strategist"}

    def __init__(self):
        self.members = {}

    def register_member(self, name, role):
        """Register a crew member with a role.

        Returns:
            tuple[bool, str]: success flag and human-readable status message.
        """
        clean_name = (name or "").strip()
        clean_role = (role or "").strip().lower()

        if not clean_name:
            return False, "Name cannot be empty."

        if clean_role not in self.VALID_ROLES:
            return False, "Role must be driver, mechanic, or strategist."

        self.members[clean_name] = clean_role
        return True, f"Registered {clean_name} as {clean_role}."

    def get_role(self, name):
        """Return role for a member name, or None if not found."""
        return self.members.get((name or "").strip())

    def list_members(self):
        """Return a copy of all registered members."""
        return dict(self.members)

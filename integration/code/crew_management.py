"""Crew management module for Street Race Manager."""

class CrewManagementModule:
    """Stores skill information for registered crew members."""

    def __init__(self):
        self.crew_stats = {}

    def assign_skill(self, name, skill_level, special_skill, registration_ref):
        """Assign skill level and special skill to an existing member."""
        clean_name = (name or "").strip()
        clean_special_skill = (special_skill or "").strip()

        if not clean_name:
            return False, "Member name cannot be empty."

        if registration_ref.get_role(clean_name) is None:
            return False, "Member must be registered before assigning skill."

        try:
            level = int(skill_level)
        except (TypeError, ValueError):
            return False, "Skill level must be an integer."

        if level < 1 or level > 100:
            return False, "Skill level must be between 1 and 100."

        if not clean_special_skill:
            return False, "Special skill cannot be empty."

        self.crew_stats[clean_name] = {
            "skill_level": level,
            "special_skill": clean_special_skill,
        }
        return True, f"Assigned skill to {clean_name}."

    def get_skill_level(self, name):
        """Get skill level for a member, or 0 if unavailable."""
        info = self.crew_stats.get((name or "").strip())
        if not info:
            return 0
        return info["skill_level"]

    def get_special_skill(self, name):
        """Get special skill for a member, or None if unavailable."""
        info = self.crew_stats.get((name or "").strip())
        if not info:
            return None
        return info["special_skill"]

    def is_driver(self, name, registration_ref):
        """Check whether a member is registered as a driver."""
        return registration_ref.get_role(name) == "driver"

    def list_skills(self):
        """Return a copy of all crew skill assignments."""
        return dict(self.crew_stats)

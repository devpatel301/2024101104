"""Power-ups module for Street Race Manager."""

class PowerUpsModule:
    """Validates and applies crew special skills as race power-ups."""

    def use_power_up(self, driver_name, power_up_name, crew_ref):
        """Return win-probability bonus if driver has the power-up."""
        clean_driver = (driver_name or "").strip()
        clean_power_up = (power_up_name or "").strip()

        if not clean_power_up:
            return 0

        current_skill = crew_ref.get_special_skill(clean_driver)
        if current_skill and current_skill.lower() == clean_power_up.lower():
            return 20

        return 0

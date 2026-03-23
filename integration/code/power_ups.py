"""Power-ups module for Street Race Manager."""

class PowerUpsModule:
    """Validates and applies crew special skills as race power-ups."""

    def has_power_up(self, driver_name, power_up_name, crew_ref):
        """Check whether the driver has the requested power-up."""
        clean_driver = (driver_name or "").strip()
        clean_power_up = (power_up_name or "").strip()
        if not clean_power_up:
            return False

        current_skill = crew_ref.get_special_skill(clean_driver)
        return bool(current_skill and current_skill.lower() == clean_power_up.lower())

    def use_power_up(self, driver_name, power_up_name, crew_ref):
        """Return whether the requested power-up can be applied."""
        return self.has_power_up(driver_name, power_up_name, crew_ref)

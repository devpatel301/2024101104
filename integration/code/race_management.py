"""Race management module for Street Race Manager."""

class RaceManagementModule:
    """Creates race context and calculates winning probability."""

    def setup_race(
        self,
        driver_name,
        car_name,
        crew_ref,
        registration_ref,
        inv_ref,
        power_up_module,
        power_up_name,
    ):
        """Validate setup and build race context data."""
        clean_driver = (driver_name or "").strip()
        clean_car = (car_name or "").strip()

        if not clean_driver or not clean_car:
            return False, "Driver and car names are required.", None

        if not crew_ref.is_driver(clean_driver, registration_ref):
            return False, "Selected member is not registered as a driver.", None

        if not inv_ref.has_car(clean_car):
            return False, "Selected car is not available in inventory.", None

        base_probability = 40
        skill_bonus = min(30, crew_ref.get_skill_level(clean_driver) // 2)
        power_up_bonus = power_up_module.use_power_up(clean_driver, power_up_name, crew_ref)
        win_probability = max(5, min(95, base_probability + skill_bonus + power_up_bonus))

        race_context = {
            "driver": clean_driver,
            "car": clean_car,
            "win_probability": win_probability,
            "power_up_bonus": power_up_bonus,
        }
        return True, "Race setup complete.", race_context

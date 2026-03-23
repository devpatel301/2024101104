"""Race management module for Street Race Manager."""

class RaceManagementModule:
    """Creates validated race context data."""

    def validate_race_entry(self, race_request, references):
        """Validate driver/car selection before building race context."""
        clean_driver = (race_request.get("driver_name") or "").strip()
        clean_car = (race_request.get("car_name") or "").strip()

        if not clean_driver or not clean_car:
            return False, "Driver and car names are required.", None, None

        if not references["crew_ref"].is_driver(clean_driver, references["registration_ref"]):
            return False, "Selected member is not registered as a driver.", None, None

        if not references["inventory_ref"].has_car(clean_car):
            return False, "Selected car is not available in inventory.", None, None

        return True, "Race entry validated.", clean_driver, clean_car

    def setup_race(self, race_request, references):
        """Validate setup and build race context data."""
        is_valid, message, clean_driver, clean_car = self.validate_race_entry(
            race_request,
            references,
        )
        if not is_valid:
            return False, message, None

        power_up_used = references["power_up_module"].has_power_up(
            clean_driver,
            race_request.get("power_up_name", ""),
            references["crew_ref"],
        )

        race_context = {
            "driver": clean_driver,
            "car": clean_car,
            "power_up_used": power_up_used,
        }
        return True, "Race setup complete.", race_context

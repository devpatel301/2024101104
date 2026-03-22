"""Mission planning module for Street Race Manager."""

class MissionPlanningModule:
    """Assigns missions and enforces role availability constraints."""

    def assign_mission(self, mission_type, target_car, registration_ref, inv_ref):
        """Assign mission and perform state updates when valid."""
        clean_mission = (mission_type or "").strip().lower()
        clean_car = (target_car or "").strip()

        if not clean_mission:
            return False, "Mission type cannot be empty."

        if clean_mission == "repair":
            has_mechanic = any(role == "mechanic" for role in registration_ref.members.values())
            if not has_mechanic:
                return False, "Repair mission needs at least one mechanic."

            ok, message = inv_ref.repair_car(clean_car)
            return ok, message

        return True, f"Mission '{clean_mission}' assigned to {clean_car}."

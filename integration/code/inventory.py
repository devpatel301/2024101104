"""Inventory module for Street Race Manager."""
class InventoryModule:
    """Tracks cash, cars, spare parts, and tools."""

    def __init__(self, starting_cash=0):
        self.cash_balance = int(starting_cash)
        self.cars = []
        self.spare_parts = []
        self.tools = []
    def update_cash(self, amount):
        """Add (or subtract) cash and return the new balance."""
        try:
            delta = int(amount)
        except (TypeError, ValueError):
            return False, "Amount must be an integer."

        if self.cash_balance + delta < 0:
            return False, "Insufficient cash balance."

        self.cash_balance += delta
        return True, f"Cash updated. Current balance: {self.cash_balance}"

    def add_item(self, category, item_name):
        """Add an item to cars, spare_parts, or tools."""
        target = self._get_category_ref(category)
        if target is None:
            return False, "Invalid category. Use cars, spare_parts, or tools."

        clean_item = (item_name or "").strip()
        if not clean_item:
            return False, "Item name cannot be empty."

        target.append(clean_item)
        return True, f"Added {clean_item} to {category}."

    def remove_item(self, category, item_name):
        """Remove an item from inventory category."""
        target = self._get_category_ref(category)
        if target is None:
            return False, "Invalid category. Use cars, spare_parts, or tools."

        clean_item = (item_name or "").strip()
        if clean_item not in target:
            return False, f"{clean_item} not found in {category}."

        target.remove(clean_item)
        return True, f"Removed {clean_item} from {category}."

    def has_car(self, car_name):
        """Return True if car is present in inventory."""
        return (car_name or "").strip() in self.cars

    def mark_car_damaged(self, car_name):
        """Append a damaged marker to the given car if present."""
        clean_car = (car_name or "").strip()
        for index, car in enumerate(self.cars):
            if car == clean_car:
                self.cars[index] = f"{car} (Damaged)"
                return True, f"Marked {clean_car} as damaged."
        return False, "Car not found in inventory."

    def repair_car(self, target_car):
        """Remove damaged marker for a car if present."""
        clean_target = (target_car or "").strip()
        damaged_name = f"{clean_target} (Damaged)"
        for index, car in enumerate(self.cars):
            if car == damaged_name:
                self.cars[index] = clean_target
                return True, f"Repaired {clean_target}."
        return False, "Target damaged car not found."

    def _get_category_ref(self, category):
        clean_category = (category or "").strip().lower()
        if clean_category == "cars":
            return self.cars
        if clean_category == "spare_parts":
            return self.spare_parts
        if clean_category == "tools":
            return self.tools
        return None

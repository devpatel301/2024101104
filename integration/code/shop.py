"""Shop module for Street Race Manager."""

class ShopModule:
    """Handles purchases of cars, parts and tools."""

    CATALOG = {
        "Basic Car": (500, "cars"),
        "Pro Car": (1200, "cars"),
        "Nitro": (150, "spare_parts"),
        "Turbo Kit": (300, "spare_parts"),
        "Toolkit": (80, "tools"),
    }

    def buy_item(self, item_name, inventory_ref):
        """Purchase an item if enough cash exists."""
        item_key = (item_name or "").strip()
        if item_key not in self.CATALOG:
            return False, "Item not available in shop catalog."

        price, category = self.CATALOG[item_key]
        if inventory_ref.cash_balance < price:
            return False, "Not enough cash to buy this item."

        ok, cash_msg = inventory_ref.update_cash(-price)
        if not ok:
            return False, cash_msg

        ok, item_msg = inventory_ref.add_item(category, item_key)
        if not ok:
            inventory_ref.update_cash(price)
            return False, item_msg

        return True, f"Bought {item_key} for {price}."

    def list_catalog(self):
        """Return copy of item catalog."""
        return dict(self.CATALOG)

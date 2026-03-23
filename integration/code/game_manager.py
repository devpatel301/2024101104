"""Main CLI loop for Street Race Manager."""

from crew_management import CrewManagementModule
from inventory import InventoryModule
from mission_planning import MissionPlanningModule
from power_ups import PowerUpsModule
from race_management import RaceManagementModule
from registration import RegistrationModule
from results import ResultsModule
from shop import ShopModule

class GameManager:
    """Runs the main CLI loop and owns module instances."""

    def __init__(self):
        self.modules = self._build_modules()

    def _build_modules(self):
        """Create and return all module instances."""
        return {
            "registration": RegistrationModule(),
            "crew": CrewManagementModule(),
            "inventory": InventoryModule(starting_cash=1000),
            "shop": ShopModule(),
            "power_ups": PowerUpsModule(),
            "race_management": RaceManagementModule(),
            "results": ResultsModule(prize_amount=200),
            "mission_planning": MissionPlanningModule(),
        }

    def execute_choice(self, choice):
        """Execute selected command and return False only when exiting."""
        handlers = {
            "1": self._handle_register_member,
            "2": self._handle_assign_skill,
            "3": self._handle_update_cash,
            "4": self._handle_add_inventory_item,
            "5": self._handle_buy_item,
            "6": self._handle_run_race,
            "7": self._handle_assign_mission,
            "8": self._print_state,
        }
        if choice == "0":
            print("Exiting Street Race Manager.")
            return False

        handler = handlers.get(choice)
        if not handler:
            print("Invalid option. Enter a number from the menu.")
            return True

        handler()
        return True

    def show_menu(self):
        """Display the main menu."""
        print("\nStreet Race Manager")
        print("1. Register crew member")
        print("2. Assign crew skill")
        print("3. Update cash")
        print("4. Add inventory item")
        print("5. Buy item from shop")
        print("6. Setup and run race")
        print("7. Assign mission")
        print("8. View system state")
        print("0. Exit")

    def run(self):
        """Run the main command-loop until user chooses to exit."""
        while True:
            self.show_menu()
            choice = input("Choose an option: ").strip()
            if not self.execute_choice(choice):
                break

    def _handle_register_member(self):
        name = input("Member name: ")
        role = input("Role (driver/mechanic/strategist): ")
        ok, message = self.modules["registration"].register_member(name, role)
        print(message)
        if not ok:
            print("Please try again.")

    def _handle_assign_skill(self):
        name = input("Member name: ")
        level = input("Skill level (1-100): ")
        special = input("Special skill / power-up name: ")
        _ok, message = self.modules["crew"].assign_skill(
            name,
            level,
            special,
            self.modules["registration"],
        )
        print(message)

    def _handle_update_cash(self):
        amount = input("Cash change (use negative to deduct): ")
        _ok, message = self.modules["inventory"].update_cash(amount)
        print(message)

    def _handle_add_inventory_item(self):
        category = input("Category (cars/spare_parts/tools): ")
        item = input("Item name: ")
        _ok, message = self.modules["inventory"].add_item(category, item)
        print(message)

    def _handle_buy_item(self):
        print("Shop Catalog:")
        for item_name, details in self.modules["shop"].list_catalog().items():
            price, category = details
            print(f"- {item_name}: {price} ({category})")
        item_name = input("Item to buy: ")
        _ok, message = self.modules["shop"].buy_item(item_name, self.modules["inventory"])
        print(message)

    def _handle_run_race(self):
        race_request = {
            "driver_name": input("Driver name: "),
            "car_name": input("Car name: "),
            "power_up_name": input("Power-up to use (leave blank for none): "),
        }
        references = {
            "crew_ref": self.modules["crew"],
            "registration_ref": self.modules["registration"],
            "inventory_ref": self.modules["inventory"],
            "power_up_module": self.modules["power_ups"],
        }
        ok, message, race_context = self.modules["race_management"].setup_race(
            race_request,
            references,
        )
        print(message)
        if ok and race_context:
            result = self.modules["results"].generate_result(
                self.modules["inventory"],
                race_context["car"],
            )
            print(f"Race roll: {result['roll']} | {result['message']}")

    def _handle_assign_mission(self):
        mission = input("Mission type (repair/other): ")
        target_car = input("Target car name: ")
        _ok, message = self.modules["mission_planning"].assign_mission(
            mission,
            target_car,
            self.modules["registration"],
            self.modules["inventory"],
        )
        print(message)

    def _print_state(self):
        """Print complete current system state."""
        print("\nCrew Members:")
        members = self.modules["registration"].list_members()
        if not members:
            print("- none")
        else:
            for name, role in members.items():
                print(f"- {name}: {role}")

        print("\nCrew Skills:")
        skills = self.modules["crew"].list_skills()
        if not skills:
            print("- none")
        else:
            for name, data in skills.items():
                print(f"- {name}: level {data['skill_level']}, special {data['special_skill']}")

        inventory = self.modules["inventory"]
        print("\nInventory:")
        print(f"- Cash: {inventory.cash_balance}")
        print(f"- Cars: {inventory.cars or ['none']}")
        print(f"- Spare Parts: {inventory.spare_parts or ['none']}")
        print(f"- Tools: {inventory.tools or ['none']}")

        print("\nRecent Results:")
        history = self.modules["results"].list_results()
        if not history:
            print("- none")
        else:
            for entry in history[-5:]:
                print(f"- Roll {entry['roll']} -> {entry['message']}")

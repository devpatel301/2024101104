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
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule()
        self.inventory = InventoryModule(starting_cash=1000)
        self.shop = ShopModule()
        self.power_ups = PowerUpsModule()
        self.race_management = RaceManagementModule()
        self.results = ResultsModule(prize_amount=200)
        self.mission_planning = MissionPlanningModule()

    def run(self):
        while True:
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
            choice = input("Choose an option: ").strip()

            if choice == "1":
                name = input("Member name: ")
                role = input("Role (driver/mechanic/strategist): ")
                ok, message = self.registration.register_member(name, role)
                print(message)
                if not ok:
                    print("Please try again.")
            elif choice == "2":
                name = input("Member name: ")
                level = input("Skill level (1-100): ")
                special = input("Special skill / power-up name: ")
                ok, message = self.crew.assign_skill(name, level, special, self.registration)
                print(message)
            elif choice == "3":
                amount = input("Cash change (use negative to deduct): ")
                ok, message = self.inventory.update_cash(amount)
                print(message)
            elif choice == "4":
                category = input("Category (cars/spare_parts/tools): ")
                item = input("Item name: ")
                ok, message = self.inventory.add_item(category, item)
                print(message)
            elif choice == "5":
                print("Shop Catalog:")
                for item_name, details in self.shop.list_catalog().items():
                    price, category = details
                    print(f"- {item_name}: {price} ({category})")
                item_name = input("Item to buy: ")
                ok, message = self.shop.buy_item(item_name, self.inventory)
                print(message)
            elif choice == "6":
                driver = input("Driver name: ")
                car = input("Car name: ")
                power_up = input("Power-up to use (leave blank for none): ")
                ok, message, race_context = self.race_management.setup_race(
                    driver,
                    car,
                    self.crew,
                    self.registration,
                    self.inventory,
                    self.power_ups,
                    power_up,
                )
                print(message)
                if ok:
                    result = self.results.generate_result(
                        race_context["win_probability"],
                        self.inventory,
                        race_context["car"],
                    )
                    print(
                        f"Race roll: {result['roll']} | Win chance: "
                        f"{result['win_probability']}% | {result['message']}"
                    )
            elif choice == "7":
                mission = input("Mission type (repair/other): ")
                target_car = input("Target car name: ")
                ok, message = self.mission_planning.assign_mission(
                    mission,
                    target_car,
                    self.registration,
                    self.inventory,
                )
                print(message)
            elif choice == "8":
                self._print_state()
            elif choice == "0":
                print("Exiting Street Race Manager.")
                break
            else:
                print("Invalid option. Enter a number from the menu.")

    def _print_state(self):
        """Print complete current system state."""
        print("\nCrew Members:")
        members = self.registration.list_members()
        if not members:
            print("- none")
        else:
            for name, role in members.items():
                print(f"- {name}: {role}")

        print("\nCrew Skills:")
        skills = self.crew.list_skills()
        if not skills:
            print("- none")
        else:
            for name, data in skills.items():
                print(
                    f"- {name}: level {data['skill_level']}, "
                    f"special {data['special_skill']}"
                )

        print("\nInventory:")
        print(f"- Cash: {self.inventory.cash_balance}")
        print(f"- Cars: {self.inventory.cars or ['none']}")
        print(f"- Spare Parts: {self.inventory.spare_parts or ['none']}")
        print(f"- Tools: {self.inventory.tools or ['none']}")

        print("\nRecent Results:")
        history = self.results.list_results()
        if not history:
            print("- none")
        else:
            for entry in history[-5:]:
                print(
                    f"- Roll {entry['roll']} vs {entry['win_probability']}%"
                    f" -> {entry['message']}"
                )

"""Main CLI loop for Street Race Manager (Task 2 incremental build)."""

from registration import RegistrationModule


class GameManager:
    """Runs the main CLI loop and owns module instances."""

    def __init__(self):
        self.registration = RegistrationModule()

    def run(self):
        while True:
            print("\nStreet Race Manager")
            print("1. Register crew member")
            print("2. View registered members")
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
                members = self.registration.list_members()
                if not members:
                    print("No members registered yet.")
                    continue
                print("Registered Crew:")
                for member_name, member_role in members.items():
                    print(f"- {member_name}: {member_role}")
            elif choice == "0":
                print("Exiting Street Race Manager.")
                break
            else:
                print("Invalid option. Enter 0, 1, or 2.")

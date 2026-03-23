# pyright: reportMissingImports=false

from conftest import build_system
from game_manager import GameManager


def _race_refs(system):
    return {
        "crew_ref": system["crew"],
        "registration_ref": system["registration"],
        "inventory_ref": system["inventory"],
        "power_up_module": system["power_ups"],
    }


def test_registration_failure_blocks_skill_assignment():
    system = build_system()
    ok, _ = system["registration"].register_member("Rhea", "medic")
    assert ok is False
    ok, message = system["crew"].assign_skill("Rhea", 50, "Nitro", system["registration"])
    assert ok is False
    assert "registered" in message.lower()


def test_invalid_skill_input_prevents_race_setup():
    system = build_system()
    system["registration"].register_member("Ari", "driver")
    ok, _ = system["crew"].assign_skill("Ari", "high", "Nitro", system["registration"])
    assert ok is False
    system["inventory"].add_item("cars", "Basic Car")
    req = {"driver_name": "Ari", "car_name": "Basic Car", "power_up_name": "Nitro"}
    ok, _msg, ctx = system["race"].setup_race(req, _race_refs(system))
    assert ok is True
    assert ctx["power_up_used"] is False


def test_unknown_shop_item_does_not_change_inventory_or_cash():
    system = build_system(starting_cash=800)
    ok, _ = system["shop"].buy_item("Unknown Item", system["inventory"])
    assert ok is False
    assert system["inventory"].cash_balance == 800
    assert system["inventory"].cars == []


def test_low_cash_prevents_buy_and_then_race_fails_for_missing_car():
    system = build_system(starting_cash=100)
    system["registration"].register_member("Ari", "driver")
    system["crew"].assign_skill("Ari", 80, "Nitro", system["registration"])
    ok, _ = system["shop"].buy_item("Basic Car", system["inventory"])
    assert ok is False
    req = {"driver_name": "Ari", "car_name": "Basic Car", "power_up_name": "Nitro"}
    ok, msg, _ = system["race"].setup_race(req, _race_refs(system))
    assert ok is False
    assert "available" in msg.lower()


def test_race_rejects_empty_driver_and_car_names():
    system = build_system()
    req = {"driver_name": " ", "car_name": "", "power_up_name": ""}
    ok, msg, _ = system["race"].setup_race(req, _race_refs(system))
    assert ok is False
    assert "required" in msg.lower()


def test_race_rejects_non_driver_even_with_car():
    system = build_system()
    system["registration"].register_member("Max", "mechanic")
    system["crew"].assign_skill("Max", 70, "Nitro", system["registration"])
    system["inventory"].add_item("cars", "Basic Car")
    req = {"driver_name": "Max", "car_name": "Basic Car", "power_up_name": "Nitro"}
    ok, msg, _ = system["race"].setup_race(req, _race_refs(system))
    assert ok is False
    assert "driver" in msg.lower()


def test_race_rejects_driver_with_unowned_car():
    system = build_system()
    system["registration"].register_member("Ari", "driver")
    system["crew"].assign_skill("Ari", 80, "Nitro", system["registration"])
    req = {"driver_name": "Ari", "car_name": "Basic Car", "power_up_name": "Nitro"}
    ok, msg, _ = system["race"].setup_race(req, _race_refs(system))
    assert ok is False
    assert "available" in msg.lower()


def test_blank_powerup_is_not_applied_in_successful_race_setup():
    system = build_system()
    system["registration"].register_member("Ari", "driver")
    system["crew"].assign_skill("Ari", 80, "Nitro", system["registration"])
    system["inventory"].add_item("cars", "Basic Car")
    req = {"driver_name": "Ari", "car_name": "Basic Car", "power_up_name": "   "}
    ok, _msg, ctx = system["race"].setup_race(req, _race_refs(system))
    assert ok is True
    assert ctx["power_up_used"] is False


def test_powerup_match_is_case_insensitive_in_race_setup():
    system = build_system()
    system["registration"].register_member("Ari", "driver")
    system["crew"].assign_skill("Ari", 100, "Nitro Boost", system["registration"])
    system["inventory"].add_item("cars", "Basic Car")
    req = {"driver_name": "Ari", "car_name": "Basic Car", "power_up_name": "nitro boost"}
    ok, _msg, ctx = system["race"].setup_race(req, _race_refs(system))
    assert ok is True
    assert ctx["power_up_used"] is True


def test_forced_win_updates_cash_and_history(monkeypatch):
    system = build_system(starting_cash=1000)
    system["registration"].register_member("Ari", "driver")
    system["crew"].assign_skill("Ari", 90, "Nitro", system["registration"])
    system["shop"].buy_item("Basic Car", system["inventory"])
    req = {"driver_name": "Ari", "car_name": "Basic Car", "power_up_name": "Nitro"}
    ok, _msg, ctx = system["race"].setup_race(req, _race_refs(system))
    assert ok is True
    monkeypatch.setattr("results.random.randint", lambda _a, _b: 1)
    result = system["results"].generate_result(system["inventory"], "Basic Car")
    assert result["win"] is True
    assert system["inventory"].cash_balance == 700
    assert len(system["results"].list_results()) == 1


def test_forced_loss_marks_car_damaged(monkeypatch):
    system = build_system()
    system["inventory"].add_item("cars", "Basic Car")
    monkeypatch.setattr("results.random.randint", lambda _a, _b: 100)
    result = system["results"].generate_result(system["inventory"], "Basic Car")
    assert result["win"] is False
    assert "Basic Car (Damaged)" in system["inventory"].cars


def test_repair_fails_without_mechanic_after_loss(monkeypatch):
    system = build_system()
    system["registration"].register_member("Ari", "driver")
    system["crew"].assign_skill("Ari", 60, "Nitro", system["registration"])
    system["inventory"].add_item("cars", "Basic Car")
    monkeypatch.setattr("results.random.randint", lambda _a, _b: 100)
    system["results"].generate_result(system["inventory"], "Basic Car")
    ok, msg = system["mission"].assign_mission(
        "repair", "Basic Car", system["registration"], system["inventory"]
    )
    assert ok is False
    assert "mechanic" in msg.lower()


def test_repair_succeeds_with_mechanic_after_loss(monkeypatch):
    system = build_system()
    system["registration"].register_member("Ari", "driver")
    system["registration"].register_member("Milo", "mechanic")
    system["crew"].assign_skill("Ari", 60, "Nitro", system["registration"])
    system["inventory"].add_item("cars", "Basic Car")
    monkeypatch.setattr("results.random.randint", lambda _a, _b: 100)
    system["results"].generate_result(system["inventory"], "Basic Car")
    ok, msg = system["mission"].assign_mission(
        "repair", "Basic Car", system["registration"], system["inventory"]
    )
    assert ok is True
    assert msg == "Repaired Basic Car."


def test_repair_fails_when_target_not_damaged_even_with_mechanic():
    system = build_system()
    system["registration"].register_member("Milo", "mechanic")
    system["inventory"].add_item("cars", "Basic Car")
    ok, msg = system["mission"].assign_mission(
        "repair", "Basic Car", system["registration"], system["inventory"]
    )
    assert ok is False
    assert "damaged" in msg.lower()


def test_non_repair_mission_succeeds_with_minimal_requirements():
    system = build_system()
    ok, msg = system["mission"].assign_mission(
        "delivery", "Basic Car", system["registration"], system["inventory"]
    )
    assert ok is True
    assert "delivery" in msg.lower()


def test_inventory_invalid_category_blocks_tooling_for_flow():
    system = build_system()
    ok, msg = system["inventory"].add_item("gadgets", "Scanner")
    assert ok is False
    assert "invalid category" in msg.lower()


def test_end_to_end_buy_lose_repair_flow(monkeypatch):
    system = build_system()
    system["registration"].register_member("Rhea", "driver")
    system["registration"].register_member("Max", "mechanic")
    system["crew"].assign_skill("Rhea", 60, "Nitro Boost", system["registration"])
    system["shop"].buy_item("Basic Car", system["inventory"])
    req = {"driver_name": "Rhea", "car_name": "Basic Car", "power_up_name": "Wrong Power"}
    ok, _msg, ctx = system["race"].setup_race(req, _race_refs(system))
    assert ok is True
    monkeypatch.setattr("results.random.randint", lambda _a, _b: 100)
    result = system["results"].generate_result(system["inventory"], ctx["car"])
    assert result["win"] is False
    ok, msg = system["mission"].assign_mission(
        "repair", "Basic Car", system["registration"], system["inventory"]
    )
    assert ok is True
    assert msg == "Repaired Basic Car."


def test_end_to_end_buy_and_win_flow(monkeypatch):
    system = build_system(starting_cash=1000)
    system["registration"].register_member("Ari", "driver")
    system["crew"].assign_skill("Ari", 90, "Nitro Boost", system["registration"])
    system["shop"].buy_item("Basic Car", system["inventory"])
    req = {"driver_name": "Ari", "car_name": "Basic Car", "power_up_name": "Nitro Boost"}
    ok, _msg, ctx = system["race"].setup_race(req, _race_refs(system))
    assert ok is True
    monkeypatch.setattr("results.random.randint", lambda _a, _b: 1)
    system["results"].generate_result(system["inventory"], ctx["car"])
    assert system["inventory"].cash_balance == 700


def test_register_driver_then_enter_race_success():
    system = build_system()
    system["registration"].register_member("Nova", "driver")
    system["crew"].assign_skill("Nova", 75, "Nitro", system["registration"])
    system["inventory"].add_item("cars", "Basic Car")
    req = {"driver_name": "Nova", "car_name": "Basic Car", "power_up_name": "Nitro"}
    ok, msg, ctx = system["race"].setup_race(req, _race_refs(system))
    assert ok is True
    assert "setup complete" in msg.lower()
    assert ctx["driver"] == "Nova"


def test_enter_race_without_registered_driver_fails():
    system = build_system()
    system["inventory"].add_item("cars", "Basic Car")
    req = {"driver_name": "Ghost", "car_name": "Basic Car", "power_up_name": "Nitro"}
    ok, msg, _ = system["race"].setup_race(req, _race_refs(system))
    assert ok is False
    assert "driver" in msg.lower() or "registered" in msg.lower()


def test_complete_race_updates_results_and_prize_money_inventory(monkeypatch):
    system = build_system(starting_cash=1000)
    system["registration"].register_member("Nova", "driver")
    system["crew"].assign_skill("Nova", 95, "Nitro", system["registration"])
    system["shop"].buy_item("Basic Car", system["inventory"])
    req = {"driver_name": "Nova", "car_name": "Basic Car", "power_up_name": "Nitro"}
    ok, _msg, ctx = system["race"].setup_race(req, _race_refs(system))
    assert ok is True
    monkeypatch.setattr("results.random.randint", lambda _a, _b: 1)
    race_result = system["results"].generate_result(system["inventory"], ctx["car"])
    assert race_result["win"] is True
    assert len(system["results"].list_results()) == 1
    assert system["inventory"].cash_balance == 700


def test_assign_mission_validates_crew_roles_for_repair():
    system = build_system()
    system["registration"].register_member("Nova", "driver")
    system["inventory"].add_item("cars", "Basic Car")
    system["inventory"].mark_car_damaged("Basic Car")

    ok, msg = system["mission"].assign_mission(
        "repair", "Basic Car", system["registration"], system["inventory"]
    )
    assert ok is False
    assert "mechanic" in msg.lower()

    system["registration"].register_member("Wren", "mechanic")
    ok, msg = system["mission"].assign_mission(
        "repair", "Basic Car", system["registration"], system["inventory"]
    )
    assert ok is True
    assert "repaired" in msg.lower()


def test_game_manager_command_register_member_updates_registry(monkeypatch):
    manager = GameManager()
    inputs = iter(["Nova", "driver"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))

    keep_running = manager.execute_choice("1")

    assert keep_running is True
    assert manager.modules["registration"].list_members().get("Nova") == "driver"


def test_game_manager_command_run_race_records_result_and_updates_cash(monkeypatch):
    manager = GameManager()
    manager.modules["registration"].register_member("Nova", "driver")
    manager.modules["crew"].assign_skill("Nova", 80, "Nitro", manager.modules["registration"])
    manager.modules["inventory"].add_item("cars", "Basic Car")

    inputs = iter(["Nova", "Basic Car", "Nitro"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))
    monkeypatch.setattr("results.random.randint", lambda _a, _b: 1)

    keep_running = manager.execute_choice("6")

    assert keep_running is True
    assert len(manager.modules["results"].list_results()) == 1
    assert manager.modules["inventory"].cash_balance == 1200


def test_game_manager_command_assign_mission_validates_roles(monkeypatch):
    manager = GameManager()
    manager.modules["inventory"].add_item("cars", "Basic Car")
    manager.modules["inventory"].mark_car_damaged("Basic Car")

    mission_inputs = iter(["repair", "Basic Car"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(mission_inputs))
    keep_running = manager.execute_choice("7")
    assert keep_running is True
    assert "Basic Car (Damaged)" in manager.modules["inventory"].cars

    register_inputs = iter(["Milo", "mechanic"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(register_inputs))
    keep_running = manager.execute_choice("1")
    assert keep_running is True

    mission_inputs = iter(["repair", "Basic Car"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(mission_inputs))
    keep_running = manager.execute_choice("7")

    assert keep_running is True
    assert "Basic Car" in manager.modules["inventory"].cars
    assert "Basic Car (Damaged)" not in manager.modules["inventory"].cars

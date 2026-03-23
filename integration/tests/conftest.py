"""Pytest configuration for integration tests."""

import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1] / "code"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from crew_management import CrewManagementModule
from inventory import InventoryModule
from mission_planning import MissionPlanningModule
from power_ups import PowerUpsModule
from race_management import RaceManagementModule
from registration import RegistrationModule
from results import ResultsModule
from shop import ShopModule

def build_system(starting_cash=1000):
    """Build fresh module instances for each test."""
    registration = RegistrationModule()
    crew = CrewManagementModule()
    inventory = InventoryModule(starting_cash=starting_cash)
    shop = ShopModule()
    power_ups = PowerUpsModule()
    race = RaceManagementModule()
    results = ResultsModule(prize_amount=200)
    mission = MissionPlanningModule()
    return {
        "registration": registration,
        "crew": crew,
        "inventory": inventory,
        "shop": shop,
        "power_ups": power_ups,
        "race": race,
        "results": results,
        "mission": mission,
    }

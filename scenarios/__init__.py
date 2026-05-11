"""POI 攻击场景模块"""
from .attack_scenarios import (
    ATTACK_SCENARIOS,
    get_scenario_by_id,
    get_scenarios_by_type,
    get_scenario_stats,
)

__all__ = [
    "ATTACK_SCENARIOS",
    "get_scenario_by_id",
    "get_scenarios_by_type",
    "get_scenario_stats",
]

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.teacher import TeacherAgent
from agents.student import StudentAgent
from core.models import AttackScenario, AttackType, Scenario, EvilCostModel, EvilRevenue


class TestTeacherAgent:
    def setup_method(self):
        self.teacher = TeacherAgent()

    def test_initial_scenario_count(self):
        assert len(self.teacher.attack_scenarios) >= 8

    def test_select_attack(self):
        attack = self.teacher.select_attack()
        assert isinstance(attack, AttackScenario)

    def test_select_attack_by_scenario(self):
        attack = self.teacher.select_attack(scenario=Scenario.UGC)
        assert attack.scenario == Scenario.UGC

    def test_generate_adversarial_sample(self):
        attack = self.teacher.select_attack()
        sample = self.teacher.generate_adversarial_sample(attack)
        assert "attack_type" in sample
        assert "expected_revenue" in sample
        assert "is_profitable" in sample

    def test_evolve_attack(self):
        original = self.teacher.select_attack()
        evolved = self.teacher.evolve_attack(original, {"detected": True})
        assert evolved.name == f"{original.name} v2"
        assert evolved.cost.bypass_difficulty == original.cost.bypass_difficulty + 1

    def test_get_all_scenarios(self):
        scenarios = self.teacher.get_all_scenarios()
        assert len(scenarios) == len(self.teacher.attack_scenarios)
        assert all("name" in s for s in scenarios)


class TestStudentAgent:
    def setup_method(self):
        self.student = StudentAgent()

    def test_initial_strategy_count(self):
        assert len(self.student.defense_strategies) >= 12

    def test_select_defense(self):
        attack = AttackScenario(
            name="AIGC 生成图",
            attack_type=AttackType.IMAGE_FORGERY,
            scenario=Scenario.UGC,
            description="Test",
        )
        strategies = self.student.select_defense(attack)
        assert len(strategies) > 0

    def test_defense_decision_block(self):
        attack = AttackScenario(
            name="UID 批量刷单",
            attack_type=AttackType.BATCH_OPERATION,
            scenario=Scenario.UGC,
            description="Test",
        )
        result = self.student.defense_decision(attack)
        assert result["action"] in ("BLOCK", "PASS")
        assert "confidence" in result

    def test_learn_from_attack(self):
        initial_count = len(self.student.defense_strategies)
        attack = AttackScenario(
            name="New Attack",
            attack_type=AttackType.IMAGE_FORGERY,
            scenario=Scenario.UGC,
            description="Test new attack",
        )
        new_strategy = self.student.learn_from_attack(attack, {})
        assert len(self.student.defense_strategies) == initial_count + 1

    def test_update_strategy(self):
        self.student.update_strategy("P 图识别", 0.95, 0.003)
        strategy = next(s for s in self.student.defense_strategies if s.name == "P 图识别")
        assert strategy.detection_rate == 0.95
        assert strategy.false_positive_rate == 0.003

    def test_get_metrics(self):
        metrics = self.student.get_metrics()
        assert "total_strategies" in metrics
        assert "effective_strategies" in metrics
        assert "avg_detection_rate" in metrics
        assert "avg_false_positive_rate" in metrics

    def test_get_all_strategies(self):
        strategies = self.student.get_all_strategies()
        assert len(strategies) == len(self.student.defense_strategies)
        assert all("name" in s and "detection_rate" in s for s in strategies)

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.models import (
    EvilCostModel, EvilRevenue, RiskCost,
    AttackScenario, AttackType, DefenseStrategy,
    AdversarialRound, Scenario, POI,
)


class TestEvilCostModel:
    def test_total_time_cost(self):
        cost = EvilCostModel(registration_time=10, operation_time=5, waiting_time=3)
        assert cost.total_time_cost() == 18

    def test_total_money_cost(self):
        cost = EvilCostModel(account_cost=5, device_cost=2, ip_cost=1)
        assert cost.total_money_cost() == 8

    def test_tech_difficulty(self):
        cost = EvilCostModel(bypass_difficulty=4, tool_dev_cost=2)
        assert cost.tech_difficulty() == 3.0

    def test_lifecycle_value(self):
        cost = EvilCostModel(account_cost=10, reuse_count=5, ban_rate=0.2)
        assert cost.lifecycle_value() == 10 * 5 * 0.8 == 40

    def test_empty_cost(self):
        cost = EvilCostModel()
        assert cost.total_time_cost() == 0
        assert cost.total_money_cost() == 0
        assert cost.tech_difficulty() == 0


class TestEvilRevenue:
    def test_expected_revenue(self):
        revenue = EvilRevenue(
            success_revenue=10000, success_rate=0.7,
            failure_loss=1000, failure_rate=0.3,
        )
        assert revenue.expected_revenue() == 10000 * 0.7 - 1000 * 0.3 == 6700.0

    def test_zero_revenue(self):
        revenue = EvilRevenue()
        assert revenue.expected_revenue() == 0.0

    def test_always_fail(self):
        revenue = EvilRevenue(
            success_revenue=10000, success_rate=0,
            failure_loss=1000, failure_rate=1.0,
        )
        assert revenue.expected_revenue() == -1000.0


class TestRiskCost:
    def test_expected_cost(self):
        risk = RiskCost(
            ban_probability=0.3, ban_loss=500,
            legal_risk=0.1, legal_loss=10000,
        )
        expected = 0.3 * 500 + 0.1 * 10000
        assert risk.expected_cost() == expected

    def test_zero_risk(self):
        risk = RiskCost()
        assert risk.expected_cost() == 0.0


class TestAttackScenario:
    def test_is_profitable(self):
        attack = AttackScenario(
            name="Test Attack",
            attack_type=AttackType.IMAGE_FORGERY,
            scenario=Scenario.UGC,
            description="Test",
            cost=EvilCostModel(
                operation_time=5,
                account_cost=0.1,
                bypass_difficulty=2,
            ),
            revenue=EvilRevenue(
                success_revenue=10000,
                success_rate=0.7,
            ),
        )
        # Should have a boolean result based on cost-revenue analysis
        assert isinstance(attack.is_profitable(), bool)

    def test_to_dict(self):
        attack = AttackScenario(
            name="Test",
            attack_type=AttackType.IMAGE_FORGERY,
            scenario=Scenario.UGC,
            description="Test attack",
        )
        d = attack.to_dict()
        assert d["name"] == "Test"
        assert d["attack_type"] == "图像伪造"
        assert d["scenario"] == "UGC"
        assert "is_profitable" in d


class TestDefenseStrategy:
    def test_effective_strategy(self):
        strategy = DefenseStrategy(
            name="Test Defense",
            description="Test",
            target_scenarios=[Scenario.UGC],
            detection_rate=0.95,
            false_positive_rate=0.005,
        )
        assert strategy.is_effective() is True

    def test_ineffective_high_fp(self):
        strategy = DefenseStrategy(
            name="Test Defense",
            description="Test",
            target_scenarios=[Scenario.UGC],
            detection_rate=0.95,
            false_positive_rate=0.05,  # > 1%
        )
        assert strategy.is_effective() is False

    def test_ineffective_low_detection(self):
        strategy = DefenseStrategy(
            name="Test Defense",
            description="Test",
            target_scenarios=[Scenario.UGC],
            detection_rate=0.7,  # < 90%
            false_positive_rate=0.005,
        )
        assert strategy.is_effective() is False


class TestAdversarialRound:
    def test_round_summary(self):
        round = AdversarialRound(
            round_id=1,
            timestamp="2026-05-11T00:00:00",
            attack_scenarios=[],
            defense_strategies=[],
            attack_success_count=2,
            defense_success_count=8,
            vulnerabilities_found=1,
            vulnerabilities_fixed=1,
            metrics={"miss_rate": 0.2, "false_positive_rate": 0.01},
        )
        summary = round.summary()
        assert "1" in summary
        assert "2" in summary
        assert "8" in summary


class TestPOI:
    def test_suspicious(self):
        poi = POI(
            poi_id="123", name="Test", address="Street",
            phone="123", brand="Brand", license_id="L123",
            creator_uid="U123", create_time="2026-01-01",
            update_time="2026-05-11",
            risk_level="high",
        )
        assert poi.is_suspicious() is True

    def test_not_suspicious(self):
        poi = POI(
            poi_id="123", name="Test", address="Street",
            phone="123", brand="Brand", license_id="L123",
            creator_uid="U123", create_time="2026-01-01",
            update_time="2026-05-11",
            risk_level="low",
        )
        assert poi.is_suspicious() is False

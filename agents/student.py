"""POI 风控对抗沙箱 - Student Agent（防御方）

人格：风控专家
动机：合规优先
行为模式:
  - 合规优先：宁可误拦，不可漏放
  - 误拦约束：误拦率 ≤ 1%（硬约束）
  - 时效优先：case 处置 ≤ 24h
"""
from typing import List, Dict
from core.models import DefenseStrategy, AttackScenario, Scenario


class StudentAgent:
    """
    Student Agent - 防御方

    模拟风控专家，基于 Teacher 的攻击生成防御策略
    """

    def __init__(self):
        self.defense_strategies: List[DefenseStrategy] = []
        self.historical_defenses: List[Dict] = []

        # 初始化 10+ 防御技能
        self._init_defense_strategies()

    def _init_defense_strategies(self):
        """初始化防御策略库"""

        # === 图像真伪检测 ===
        self.defense_strategies.append(DefenseStrategy(
            name="P 图识别",
            description="检测 PS 篡改的营业执照/门头照",
            target_scenarios=[Scenario.BGC],
            detection_rate=0.92,
            false_positive_rate=0.005,
        ))

        self.defense_strategies.append(DefenseStrategy(
            name="AIGC 检测",
            description="检测 Midjourney/Stable Diffusion 生成的虚假图片",
            target_scenarios=[Scenario.UGC],
            detection_rate=0.88,
            false_positive_rate=0.008,
        ))

        self.defense_strategies.append(DefenseStrategy(
            name="视频伪造检测",
            description="检测一镜到底视频伪造",
            target_scenarios=[Scenario.UGC],
            detection_rate=0.85,
            false_positive_rate=0.01,
        ))

        # === 批量操作识别 ===
        self.defense_strategies.append(DefenseStrategy(
            name="UID 关联分析",
            description="识别同一 UID 批量新增/篡改行为",
            target_scenarios=[Scenario.UGC, Scenario.BGC],
            detection_rate=0.95,
            false_positive_rate=0.003,
        ))

        self.defense_strategies.append(DefenseStrategy(
            name="设备指纹识别",
            description="基于设备指纹的批量操作识别",
            target_scenarios=[Scenario.UGC, Scenario.BGC],
            detection_rate=0.93,
            false_positive_rate=0.005,
        ))

        self.defense_strategies.append(DefenseStrategy(
            name="IP 聚类分析",
            description="基于 IP 聚类的异常行为检测",
            target_scenarios=[Scenario.UGC, Scenario.BGC],
            detection_rate=0.90,
            false_positive_rate=0.008,
        ))

        # === 信息篡改检测 ===
        self.defense_strategies.append(DefenseStrategy(
            name="电话异常检测",
            description="检测电话号码异常变更",
            target_scenarios=[Scenario.BGC],
            detection_rate=0.94,
            false_positive_rate=0.006,
        ))

        self.defense_strategies.append(DefenseStrategy(
            name="地址异常检测",
            description="检测地址异常变更",
            target_scenarios=[Scenario.BGC],
            detection_rate=0.91,
            false_positive_rate=0.007,
        ))

        self.defense_strategies.append(DefenseStrategy(
            name="品牌异常检测",
            description="检测品牌信息异常变更",
            target_scenarios=[Scenario.BGC],
            detection_rate=0.89,
            false_positive_rate=0.008,
        ))

        # === 资质核验 ===
        self.defense_strategies.append(DefenseStrategy(
            name="营业执照 OCR",
            description="营业执照 OCR 识别 + 核验",
            target_scenarios=[Scenario.BGC],
            detection_rate=0.96,
            false_positive_rate=0.002,
        ))

        self.defense_strategies.append(DefenseStrategy(
            name="一照多检",
            description="检测一张执照注册多个点位",
            target_scenarios=[Scenario.BGC],
            detection_rate=0.97,
            false_positive_rate=0.001,
        ))

        # === 多源交叉验证 ===
        self.defense_strategies.append(DefenseStrategy(
            name="互联网发现",
            description="基于互联网信息的多源交叉验证",
            target_scenarios=[Scenario.NON_UB],
            detection_rate=0.85,
            false_positive_rate=0.01,
        ))

        self.defense_strategies.append(DefenseStrategy(
            name="智能外呼",
            description="智能外呼联系商家验证",
            target_scenarios=[Scenario.NON_UB],
            detection_rate=0.92,
            false_positive_rate=0.005,
        ))

    def select_defense(self, attack: AttackScenario) -> List[DefenseStrategy]:
        """
        选择防御策略

        基于攻击类型选择合适的防御策略
        """
        matching_strategies = [
            s for s in self.defense_strategies
            if attack.scenario in s.target_scenarios
        ]

        # 返回所有有效的防御策略
        return [s for s in matching_strategies if s.is_effective()]

    def defense_decision(self, attack: AttackScenario,
                         context: Dict = None) -> Dict:
        """
        防御决策

        返回：是否拦截、使用哪些策略、置信度
        """
        strategies = self.select_defense(attack)

        if not strategies:
            return {
                "action": "PASS",
                "reason": "无匹配防御策略",
                "confidence": 0,
            }

        # 综合置信度
        avg_detection = sum(s.detection_rate for s in strategies) / len(strategies)
        avg_fp = sum(s.false_positive_rate for s in strategies) / len(strategies)

        # 决策：置信度 > 阈值则拦截
        threshold = 0.85
        if avg_detection >= threshold:
            return {
                "action": "BLOCK",
                "reason": f"触发{len(strategies)}个防御策略",
                "strategies": [s.name for s in strategies],
                "confidence": avg_detection,
                "false_positive_rate": avg_fp,
            }
        else:
            return {
                "action": "PASS",
                "reason": "置信度不足",
                "confidence": avg_detection,
            }

    def learn_from_attack(self, attack: AttackScenario,
                          defense_result: Dict) -> DefenseStrategy:
        """
        从攻击中学习，生成新防御策略
        """
        # 简单学习：针对新攻击类型增加检测能力
        new_strategy = DefenseStrategy(
            name=f"针对{attack.name}检测",
            description=f"专门检测 {attack.description}",
            target_scenarios=[attack.scenario],
            detection_rate=0.85,  # 初始检测率
            false_positive_rate=0.01,
        )

        self.defense_strategies.append(new_strategy)
        return new_strategy

    def update_strategy(self, strategy_name: str,
                        new_detection_rate: float,
                        new_fp_rate: float):
        """更新防御策略参数"""
        for s in self.defense_strategies:
            if s.name == strategy_name:
                s.detection_rate = new_detection_rate
                s.false_positive_rate = new_fp_rate
                break

    def get_metrics(self) -> Dict:
        """获取当前指标"""
        effective_count = sum(1 for s in self.defense_strategies if s.is_effective())
        return {
            "total_strategies": len(self.defense_strategies),
            "effective_strategies": effective_count,
            "avg_detection_rate": sum(s.detection_rate for s in self.defense_strategies) / len(self.defense_strategies),
            "avg_false_positive_rate": sum(s.false_positive_rate for s in self.defense_strategies) / len(self.defense_strategies),
        }

    def get_all_strategies(self) -> List[Dict]:
        """获取所有防御策略"""
        return [
            {
                "name": s.name,
                "description": s.description,
                "target_scenarios": [sc.value for sc in s.target_scenarios],
                "detection_rate": s.detection_rate,
                "false_positive_rate": s.false_positive_rate,
                "is_effective": s.is_effective(),
            }
            for s in self.defense_strategies
        ]


if __name__ == "__main__":
    from core.models import AttackScenario, AttackType, Scenario

    student = StudentAgent()

    print("=" * 50)
    print("Student Agent - 防御方")
    print("=" * 50)

    # 获取指标
    metrics = student.get_metrics()
    print(f"\n防御策略总数：{metrics['total_strategies']}")
    print(f"有效策略数：{metrics['effective_strategies']}")
    print(f"平均检测率：{metrics['avg_detection_rate']:.2%}")
    print(f"平均误报率：{metrics['avg_false_positive_rate']:.2%}")

    # 模拟防御决策
    attack = AttackScenario(
        name="AIGC 生成图",
        attack_type=AttackType.IMAGE_FORGERY,
        scenario=Scenario.UGC,
        description="测试攻击",
    )

    result = student.defense_decision(attack)
    print(f"\n防御决策：{result['action']}")
    print(f"原因：{result['reason']}")
    print(f"置信度：{result.get('confidence', 0):.2%}")

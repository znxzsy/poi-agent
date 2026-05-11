"""POI 风控对抗沙箱 - Teacher Agent（攻击方）

人格：黑灰产从业者
动机：利益驱动
行为模式：
  - 成本收益计算：每次攻击前评估投入产出比
  - 风险规避：优先选择低风险攻击方式
  - 边界探索：持续试探平台风控边界
"""
from typing import List, Dict
from core.models import AttackScenario, AttackType, Scenario, EvilCostModel, EvilRevenue, RiskCost


class TeacherAgent:
    """
    Teacher Agent - 攻击方

    模拟黑灰产从业者，从作恶动机出发，持续生成对抗样本
    """

    def __init__(self):
        self.attack_scenarios: List[AttackScenario] = []
        self.historical_attacks: List[AttackScenario] = []
        self.cost_model = {}

        # 初始化 20+ 攻击场景
        self._init_attack_scenarios()

    def _init_attack_scenarios(self):
        """初始化攻击场景库"""

        # === 图像伪造 ===
        self.attack_scenarios.append(AttackScenario(
            name="P 图篡改",
            attack_type=AttackType.IMAGE_FORGERY,
            scenario=Scenario.BGC,
            description="用 PS 篡改营业执照/门头照",
            cost=EvilCostModel(
                operation_time=30,
                bypass_difficulty=3,
                tool_dev_cost=1,
            ),
            revenue=EvilRevenue(
                success_revenue=5000,
                success_rate=0.5,
            ),
        ))

        self.attack_scenarios.append(AttackScenario(
            name="AIGC 生成图",
            attack_type=AttackType.IMAGE_FORGERY,
            scenario=Scenario.UGC,
            description="用 Midjourney/Stable Diffusion 生成虚假门店图",
            cost=EvilCostModel(
                operation_time=5,
                account_cost=0.1,
                bypass_difficulty=2,
            ),
            revenue=EvilRevenue(
                success_revenue=10000,
                success_rate=0.7,
            ),
        ))

        self.attack_scenarios.append(AttackScenario(
            name="一镜到底视频伪造",
            attack_type=AttackType.IMAGE_FORGERY,
            scenario=Scenario.UGC,
            description="用视频编辑工具伪造探店视频",
            cost=EvilCostModel(
                operation_time=60,
                bypass_difficulty=5,
                tool_dev_cost=3,
            ),
            revenue=EvilRevenue(
                success_revenue=8000,
                success_rate=0.4,
            ),
        ))

        # === 批量操作 ===
        self.attack_scenarios.append(AttackScenario(
            name="UID 批量刷单",
            attack_type=AttackType.BATCH_OPERATION,
            scenario=Scenario.UGC,
            description="一个 UID 批量新增/篡改多个点位",
            cost=EvilCostModel(
                registration_time=10,
                operation_time=2,
                account_cost=5,
                ban_rate=0.3,
                reuse_count=50,
            ),
            revenue=EvilRevenue(
                success_revenue=50000,
                success_rate=0.6,
            ),
        ))

        # === 信息篡改 ===
        self.attack_scenarios.append(AttackScenario(
            name="恶意篡改电话",
            attack_type=AttackType.INFO_TAMPERING,
            scenario=Scenario.BGC,
            description="把商家电话改成自己的引流电话",
            cost=EvilCostModel(
                operation_time=5,
                bypass_difficulty=2,
            ),
            revenue=EvilRevenue(
                success_revenue=5000,
                success_rate=0.4,
            ),
        ))

        self.attack_scenarios.append(AttackScenario(
            name="恶意篡改地址",
            attack_type=AttackType.INFO_TAMPERING,
            scenario=Scenario.BGC,
            description="把地址改成相近位置，截流客户",
            cost=EvilCostModel(
                operation_time=5,
                bypass_difficulty=3,
            ),
            revenue=EvilRevenue(
                success_revenue=3000,
                success_rate=0.3,
            ),
        ))

        self.attack_scenarios.append(AttackScenario(
            name="恶意篡改品牌",
            attack_type=AttackType.INFO_TAMPERING,
            scenario=Scenario.BGC,
            description="把小品牌改成知名品牌，蹭流量",
            cost=EvilCostModel(
                operation_time=5,
                bypass_difficulty=4,
            ),
            revenue=EvilRevenue(
                success_revenue=10000,
                success_rate=0.2,
            ),
        ))

        # === 资质造假 ===
        self.attack_scenarios.append(AttackScenario(
            name="营业执照一对多",
            attack_type=AttackType.QUALITY_FRAUD,
            scenario=Scenario.BGC,
            description="一张执照注册多个点位",
            cost=EvilCostModel(
                operation_time=10,
                bypass_difficulty=3,
            ),
            revenue=EvilRevenue(
                success_revenue=2000,
                success_rate=0.5,
            ),
        ))

        # === 擦边违规 ===
        self.attack_scenarios.append(AttackScenario(
            name="挂品信息擦边",
            attack_type=AttackType.BORDERLINE,
            scenario=Scenario.BGC,
            description="黄赌毒等违规内容",
            cost=EvilCostModel(
                operation_time=5,
                bypass_difficulty=6,
            ),
            revenue=EvilRevenue(
                success_revenue=20000,
                success_rate=0.1,
                failure_loss=50000,
                failure_rate=0.9,
            ),
            risk=RiskCost(
                ban_probability=0.9,
                ban_loss=50000,
                legal_risk=0.5,
                legal_loss=100000,
            ),
        ))

    def select_attack(self, scenario: Scenario = None) -> AttackScenario:
        """
        选择最优攻击方式

        决策逻辑：argmax(收益 - 成本 - 风险)
        """
        candidates = self.attack_scenarios
        if scenario:
            candidates = [s for s in candidates if s.scenario == scenario]

        # 选择最有利可图的攻击
        profitable_attacks = [a for a in candidates if a.is_profitable()]
        if profitable_attacks:
            # 按期望收益排序
            return max(profitable_attacks,
                       key=lambda x: x.revenue.expected_revenue())

        # 如果没有有利可图的，选择成本最低的
        return min(candidates,
                   key=lambda x: x.cost.total_money_cost())

    def generate_adversarial_sample(self, attack: AttackScenario) -> Dict:
        """生成对抗样本"""
        return {
            "attack_type": attack.attack_type.value,
            "scenario": attack.scenario.value,
            "description": attack.description,
            "cost": {
                "time": attack.cost.total_time_cost(),
                "money": attack.cost.total_money_cost(),
                "tech": attack.cost.tech_difficulty(),
            },
            "expected_revenue": attack.revenue.expected_revenue(),
            "is_profitable": attack.is_profitable(),
        }

    def evolve_attack(self, old_attack: AttackScenario,
                      defense_info: Dict) -> AttackScenario:
        """
        演进攻击方式

        基于防御方的策略，调整攻击方式以绕过检测
        """
        # 简单演进：增加技术难度，降低被检测率
        evolved = AttackScenario(
            name=f"{old_attack.name} v2",
            attack_type=old_attack.attack_type,
            scenario=old_attack.scenario,
            description=f"升级版：{old_attack.description}",
            cost=EvilCostModel(
                operation_time=old_attack.cost.operation_time * 1.2,
                account_cost=old_attack.cost.account_cost * 1.1,
                bypass_difficulty=old_attack.cost.bypass_difficulty + 1,
                tool_dev_cost=old_attack.cost.tool_dev_cost + 1,
            ),
            revenue=EvilRevenue(
                success_revenue=old_attack.revenue.success_revenue,
                success_rate=old_attack.revenue.success_rate * 0.8,  # 成功率下降
            ),
        )
        return evolved

    def get_all_scenarios(self) -> List[Dict]:
        """获取所有攻击场景"""
        return [s.to_dict() for s in self.attack_scenarios]


if __name__ == "__main__":
    teacher = TeacherAgent()

    print("=" * 50)
    print("Teacher Agent - 攻击方")
    print("=" * 50)

    # 选择最优攻击
    best_attack = teacher.select_attack(Scenario.UGC)
    print(f"\n最优攻击方式：{best_attack.name}")
    print(f"期望收益：￥{best_attack.revenue.expected_revenue():.2f}")
    print(f"是否有利可图：{best_attack.is_profitable()}")

    # 生成对抗样本
    sample = teacher.generate_adversarial_sample(best_attack)
    print(f"\n对抗样本：{sample}")

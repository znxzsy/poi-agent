"""POI 风控对抗沙箱 - 核心数据模型"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional
import json


class AttackType(Enum):
    """攻击类型枚举"""
    IMAGE_FORGERY = "图像伪造"  # P 图/AIGC 生成图/视频伪造
    BATCH_OPERATION = "批量操作"  # UID 批量刷单
    INFO_TAMPERING = "信息篡改"  # 篡改电话/地址/品牌
    QUALITY_FRAUD = "资质造假"  # 营业执照一对多
    BORDERLINE = "擦边违规"  # 挂品信息擦边


class Scenario(Enum):
    """场景枚举"""
    UGC = "UGC"  # 用户生成内容
    BGC = "BGC"  # 商家生成内容
    NON_UB = "非 UB"  # 非用户/商家生成


@dataclass
class EvilCostModel:
    """
    作恶成本四维模型

    核心公式：作恶成本 = 时间成本 + 资金成本 + 技术成本 + 账号成本
    平台目标：作恶成本 > 作恶收益
    """
    # 时间成本（分钟）
    registration_time: float = 0  # 注册耗时
    operation_time: float = 0  # 操作耗时
    waiting_time: float = 0  # 等待耗时

    # 资金成本（元）
    account_cost: float = 0  # 账号成本
    device_cost: float = 0  # 设备成本
    ip_cost: float = 0  # IP 成本

    # 技术成本（1-10 难度等级）
    bypass_difficulty: float = 0  # 绕过难度
    tool_dev_cost: float = 0  # 工具开发成本

    # 账号成本
    ban_rate: float = 0  # 封号率 (0-1)
    reuse_count: int = 0  # 复用次数

    def total_time_cost(self) -> float:
        """总时间成本（分钟）"""
        return self.registration_time + self.operation_time + self.waiting_time

    def total_money_cost(self) -> float:
        """总资金成本（元）"""
        return self.account_cost + self.device_cost + self.ip_cost

    def tech_difficulty(self) -> float:
        """技术难度平均值"""
        return (self.bypass_difficulty + self.tool_dev_cost) / 2

    def account lifecycle_value(self) -> float:
        """账号生命周期价值"""
        return self.account_cost * self.reuse_count * (1 - self.ban_rate)


@dataclass
class EvilRevenue:
    """
    作恶收益模型

    作恶收益 = 成功收益 × 成功率 - 失败损失 × 失败率
    """
    success_revenue: float = 0  # 成功收益
    success_rate: float = 0  # 成功率 (0-1)
    failure_loss: float = 0  # 失败损失
    failure_rate: float = 0  # 失败率 (0-1)

    def expected_revenue(self) -> float:
        """期望收益"""
        return (self.success_revenue * self.success_rate -
                self.failure_loss * self.failure_rate)


@dataclass
class RiskCost:
    """
    风险成本模型

    风险成本 = 被封概率 × 封禁损失 + 法律风险 × 法律损失
    """
    ban_probability: float = 0  # 被封概率 (0-1)
    ban_loss: float = 0  # 封禁损失
    legal_risk: float = 0  # 法律风险 (0-1)
    legal_loss: float = 0  # 法律损失

    def expected_cost(self) -> float:
        """期望风险成本"""
        return (self.ban_probability * self.ban_loss +
                self.legal_risk * self.legal_loss)


@dataclass
class AttackScenario:
    """
    攻击场景定义

    所有黑灰产攻击归根结底就两件事：
    1. 增了假的点 → 无中生有
    2. 篡改属性 → 把别人的信息改成自己的
    """
    name: str  # 场景名称
    attack_type: AttackType  # 攻击类型
    scenario: Scenario  # 适用场景
    description: str  # 描述

    # 成本参数
    cost: EvilCostModel = field(default_factory=EvilCostModel)

    # 收益参数
    revenue: EvilRevenue = field(default_factory=EvilRevenue)

    # 风险参数
    risk: RiskCost = field(default_factory=RiskCost)

    # 历史数据
    historical_success_rate: float = 0  # 历史成功率
    detection_rate: float = 0  # 被检测率

    def is_profitable(self) -> bool:
        """是否有利可图"""
        total_cost = (self.cost.total_money_cost() +
                      self.cost.total_time_cost() * 0.1 +  # 时间折算
                      self.cost.tech_difficulty() * 100)  # 技术难度折算
        expected_revenue = self.revenue.expected_revenue()
        risk_cost = self.risk.expected_cost()

        return expected_revenue > (total_cost + risk_cost)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "attack_type": self.attack_type.value,
            "scenario": self.scenario.value,
            "description": self.description,
            "is_profitable": self.is_profitable(),
        }


@dataclass
class DefenseStrategy:
    """防御策略"""
    name: str
    description: str
    target_scenarios: List[Scenario]

    # 防御效果
    detection_rate: float = 0  # 检测率
    false_positive_rate: float = 0  # 误报率

    # 约束条件
    max_false_positive: float = 0.01  # 误拦率≤1%

    def is_effective(self) -> bool:
        """是否有效"""
        return (self.detection_rate >= 0.9 and
                self.false_positive_rate <= self.max_false_positive)


@dataclass
class对抗 Round:
    """对抗轮次"""
    round_id: int
    timestamp: str

    # 攻击方
    attack_scenarios: List[AttackScenario]
    attack_success_count: int = 0

    # 防御方
    defense_strategies: List[DefenseStrategy]
    defense_success_count: int = 0

    # 结果
    vulnerabilities_found: int = 0
    vulnerabilities_fixed: int = 0

    # 指标
    metrics: Dict = field(default_factory=dict)

    def summary(self) -> str:
        return f"""
┌─────────────────────────────────────────────┐
│  第 {self.round_id} 轮对抗结果
├─────────────────────────────────────────────┤
│  攻击成功：{self.attack_success_count} | 防御成功：{self.defense_success_count}
│  发现漏洞：{self.vulnerabilities_found} | 修复漏洞：{self.vulnerabilities_fixed}
│  漏放率：{self.metrics.get('miss_rate', 0):.2%} | 误拦率：{self.metrics.get('false_positive_rate', 0):.2%}
└─────────────────────────────────────────────┘
"""


@dataclass
class POI:
    """POI 点位"""
    poi_id: str
    name: str
    address: str
    phone: str
    brand: str
    license_id: str  # 营业执照 ID

    # 元数据
    creator_uid: str
    create_time: str
    update_time: str

    # 状态
    status: str = "active"  # active/suspended/removed
    risk_level: str = "low"  # low/medium/high

    def is_suspicious(self) -> bool:
        """是否可疑"""
        return self.risk_level in ["medium", "high"]


if __name__ == "__main__":
    # 示例：创建一个攻击场景
    attack = AttackScenario(
        name="AIGC 生成图 + 批量刷单",
        attack_type=AttackType.IMAGE_FORGERY,
        scenario=Scenario.UGC,
        description="用 Midjourney 生成虚假门店图片，批量注册 UID 新增虚假 POI",
        cost=EvilCostModel(
            registration_time=10,
            operation_time=5,
            account_cost=5,
            ban_rate=0.3,
            reuse_count=10,
        ),
        revenue=EvilRevenue(
            success_revenue=50000,
            success_rate=0.6,
            failure_loss=1000,
            failure_rate=0.4,
        ),
        risk=RiskCost(
            ban_probability=0.3,
            ban_loss=500,
        ),
    )

    print(f"攻击场景：{attack.name}")
    print(f"是否有利可图：{attack.is_profitable()}")
    print(f"期望收益：￥{attack.revenue.expected_revenue():.2f}")

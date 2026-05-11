"""POI 攻击场景定义

基于真实对抗数据沉淀的攻击场景库
每个场景包含：攻击手法、成本收益模型、历史成功率
"""

# 攻击场景库
ATTACK_SCENARIOS = [
    {
        "scenario_id": "ATK_NAME_TAMPER_001",
        "scenario_name": "名称篡改 - 品牌蹭流",
        "attack_type": "INFO_TAMPERING",
        "scenario_type": "BGC",

        "description": "将知名商家名称改为相似或知名品牌，蹭取流量",

        "attack_pattern": {
            "target_field": "poi_name",
            "change_type": "complete_replace",
            "common_patterns": [
                "移除前缀品牌词",
                "添加知名连锁品牌后缀",
                "使用谐音字替代",
            ]
        },

        "cost_model": {
            # 时间成本（分钟）
            "registration_time": 5,      # 注册账号
            "operation_time": 3,         # 提交变更
            "waiting_time": 120,         # 等待审核

            # 资金成本（元）
            "account_cost": 5,           # 账号成本
            "device_cost": 0,            # 设备成本
            "ip_cost": 0,                # IP 成本

            # 技术成本（1-10）
            "bypass_difficulty": 3,      # 绕过难度中等
            "tool_dev_cost": 1,          # 无需工具开发
        },

        "revenue_model": {
            "success_revenue": 8000,     # 成功引流收益
            "success_rate": 0.35,        # 历史成功率
            "failure_loss": 500,         # 失败损失（封号）
            "failure_rate": 0.65,        # 失败率
        },

        "risk_model": {
            "ban_probability": 0.4,      # 被封概率
            "ban_loss": 2000,            # 封号损失
            "legal_risk": 0.1,           # 法律风险低
            "legal_loss": 5000,          # 法律损失
        },

        # 历史对抗数据
        "historical_stats": {
            "total_attempts": 156,
            "success_count": 55,
            "detected_count": 101,
            "avg_detection_rate": 0.647,
        },

        "example_task_ids": [
            "audit_ti_d3a75b98488744d39b3a099c6b1af45a",
        ],
    },

    {
        "scenario_id": "ATK_PHONE_TAMPER_001",
        "scenario_name": "电话篡改 - 引流欺诈",
        "attack_type": "INFO_TAMPERING",
        "scenario_type": "BGC",

        "description": "将商家电话改为自己的引流电话，截获客户咨询",

        "attack_pattern": {
            "target_field": "telephone",
            "change_type": "complete_replace",
            "common_patterns": [
                "座机改手机",
                "外地号码替换本地号码",
                "虚拟号码替换真实号码",
            ]
        },

        "cost_model": {
            "registration_time": 5,
            "operation_time": 2,
            "waiting_time": 60,
            "account_cost": 5,
            "device_cost": 0,
            "ip_cost": 0,
            "bypass_difficulty": 4,
            "tool_dev_cost": 1,
        },

        "revenue_model": {
            "success_revenue": 5000,
            "success_rate": 0.42,
            "failure_loss": 300,
            "failure_rate": 0.58,
        },

        "risk_model": {
            "ban_probability": 0.35,
            "ban_loss": 1500,
            "legal_risk": 0.15,
            "legal_loss": 8000,
        },

        "historical_stats": {
            "total_attempts": 234,
            "success_count": 98,
            "detected_count": 136,
            "avg_detection_rate": 0.581,
        },
    },

    {
        "scenario_id": "ATK_PHOTO_REMOVE_001",
        "scenario_name": "门头照移除 - 规避核实",
        "attack_type": "IMAGE_FORGERY",
        "scenario_type": "BGC",

        "description": "移除原有门头照，使审核人员无法核实名称变更真实性",

        "attack_pattern": {
            "target_field": "store_photo",
            "change_type": "remove_all",
            "common_patterns": [
                "清空所有门头照",
                "替换为模糊图片",
                "替换为无关场景图",
            ]
        },

        "cost_model": {
            "registration_time": 5,
            "operation_time": 2,
            "waiting_time": 120,
            "account_cost": 5,
            "device_cost": 0,
            "ip_cost": 0,
            "bypass_difficulty": 5,
            "tool_dev_cost": 2,
        },

        "revenue_model": {
            "success_revenue": 6000,
            "success_rate": 0.28,
            "failure_loss": 400,
            "failure_rate": 0.72,
        },

        "risk_model": {
            "ban_probability": 0.5,
            "ban_loss": 1800,
            "legal_risk": 0.08,
            "legal_loss": 3000,
        },

        "historical_stats": {
            "total_attempts": 89,
            "success_count": 25,
            "detected_count": 64,
            "avg_detection_rate": 0.719,
        },
    },

    {
        "scenario_id": "ATK_ADDRESS_SHIFT_001",
        "scenario_name": "地址微调 - 位置劫持",
        "attack_type": "INFO_TAMPERING",
        "scenario_type": "BGC",

        "description": "对地址进行微小修改（如添加楼层、房间号），实现位置劫持",

        "attack_pattern": {
            "target_field": "address",
            "change_type": "minor_modification",
            "common_patterns": [
                "添加楼层信息",
                "修改门牌号数字",
                "添加/删除方位词",
            ]
        },

        "cost_model": {
            "registration_time": 5,
            "operation_time": 2,
            "waiting_time": 60,
            "account_cost": 5,
            "device_cost": 0,
            "ip_cost": 0,
            "bypass_difficulty": 2,
            "tool_dev_cost": 1,
        },

        "revenue_model": {
            "success_revenue": 3000,
            "success_rate": 0.55,
            "failure_loss": 200,
            "failure_rate": 0.45,
        },

        "risk_model": {
            "ban_probability": 0.25,
            "ban_loss": 1000,
            "legal_risk": 0.05,
            "legal_loss": 2000,
        },

        "historical_stats": {
            "total_attempts": 312,
            "success_count": 172,
            "detected_count": 140,
            "avg_detection_rate": 0.449,
        },
    },

    {
        "scenario_id": "ATK_COORDINATE_DRIFT_001",
        "scenario_name": "坐标漂移 - 位置偏移",
        "attack_type": "INFO_TAMPERING",
        "scenario_type": "BGC",

        "description": "微调经纬度坐标，使 POI 显示在相邻位置",

        "attack_pattern": {
            "target_field": "coordinate",
            "change_type": "coordinate_drift",
            "common_patterns": [
                "小范围偏移（<100 米）",
                "偏移到相邻商铺",
                "偏移到同楼不同层",
            ]
        },

        "cost_model": {
            "registration_time": 5,
            "operation_time": 5,
            "waiting_time": 120,
            "account_cost": 5,
            "device_cost": 0,
            "ip_cost": 0,
            "bypass_difficulty": 6,
            "tool_dev_cost": 3,
        },

        "revenue_model": {
            "success_revenue": 10000,
            "success_rate": 0.18,
            "failure_loss": 800,
            "failure_rate": 0.82,
        },

        "risk_model": {
            "ban_probability": 0.65,
            "ban_loss": 2500,
            "legal_risk": 0.2,
            "legal_loss": 10000,
        },

        "historical_stats": {
            "total_attempts": 67,
            "success_count": 12,
            "detected_count": 55,
            "avg_detection_rate": 0.821,
        },
    },
]


def get_scenario_by_id(scenario_id: str) -> dict:
    """根据 ID 获取攻击场景"""
    for s in ATTACK_SCENARIOS:
        if s["scenario_id"] == scenario_id:
            return s
    return None


def get_scenarios_by_type(attack_type: str) -> list:
    """根据攻击类型获取场景列表"""
    return [s for s in ATTACK_SCENARIOS if s["attack_type"] == attack_type]


def get_scenario_stats() -> dict:
    """获取攻击场景统计"""
    total = len(ATTACK_SCENARIOS)
    total_attempts = sum(s["historical_stats"]["total_attempts"] for s in ATTACK_SCENARIOS)
    total_success = sum(s["historical_stats"]["success_count"] for s in ATTACK_SCENARIOS)

    return {
        "scenario_count": total,
        "total_attempts": total_attempts,
        "total_success": total_success,
        "avg_success_rate": total_success / total_attempts if total_attempts > 0 else 0,
    }


if __name__ == "__main__":
    print("=== POI 攻击场景库 ===\n")
    for scenario in ATTACK_SCENARIOS:
        print(f"[{scenario['scenario_id']}] {scenario['scenario_name']}")
        print(f"  攻击类型：{scenario['attack_type']}")
        print(f"  成功率：{scenario['revenue_model']['success_rate']:.1%}")
        print(f"  历史检测率：{scenario['historical_stats']['avg_detection_rate']:.1%}")
        print()

    stats = get_scenario_stats()
    print(f"=== 统计汇总 ===")
    print(f"场景总数：{stats['scenario_count']}")
    print(f"历史攻击次数：{stats['total_attempts']}")
    print(f"平均成功率：{stats['avg_success_rate']:.1%}")

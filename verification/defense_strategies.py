"""验证层 - 防御策略与验证结果

包含防御策略定义和验证结果记录
"""

# 防御策略库
DEFENSE_STRATEGIES = [
    {
        "strategy_id": "DEF_NAME_CHECK_001",
        "strategy_name": "名称变更检测",
        "description": "检测 POI 名称异常变更，包括品牌词移除/添加、谐音字替换等",

        "target_fields": ["poi_name"],
        "target_attack_types": ["INFO_TAMPERING"],

        "detection_rules": [
            {
                "rule_id": "NAME_BRAND_REMOVAL",
                "rule_name": "品牌词移除检测",
                "condition": "old_name contains brand_keyword AND new_name NOT contains brand_keyword",
                "weight": 0.35,
            },
            {
                "rule_id": "NAME_SIMILARITY_CHECK",
                "rule_name": "名称相似度检测",
                "condition": "levenshtein_distance(old, new) / max_len > 0.6",
                "weight": 0.30,
            },
            {
                "rule_id": "NAME_HOMO PHONE_CHECK",
                "rule_name": "谐音字检测",
                "condition": "pinyin_similarity(old, new) > 0.8 AND char_diff > 1",
                "weight": 0.35,
            },
        ],

        "performance": {
            "detection_rate": 0.85,
            "false_positive_rate": 0.008,
            "avg_confidence": 0.78,
        },

        "threshold": 0.70,
        "is_active": True,
    },

    {
        "strategy_id": "DEF_PHONE_RISK_001",
        "strategy_name": "电话风险评估",
        "description": "评估电话变更风险，包括号码类型变化、归属地变化、号码段风险等",

        "target_fields": ["telephone"],
        "target_attack_types": ["INFO_TAMPERING"],

        "detection_rules": [
            {
                "rule_id": "PHONE_TYPE_CHANGE",
                "rule_name": "号码类型变化检测",
                "condition": "old_type != new_type (e.g., landline -> mobile)",
                "weight": 0.40,
            },
            {
                "rule_id": "PHONE_AREA_CHANGE",
                "rule_name": "归属地变化检测",
                "condition": "old_area_code != new_area_code",
                "weight": 0.30,
            },
            {
                "rule_id": "PHONE_RISK_SEGMENT",
                "rule_name": "高风险号段检测",
                "condition": "new_phone in risk_segment_list",
                "weight": 0.30,
            },
        ],

        "performance": {
            "detection_rate": 0.72,
            "false_positive_rate": 0.012,
            "avg_confidence": 0.65,
        },

        "threshold": 0.60,
        "is_active": True,
    },

    {
        "strategy_id": "DEF_PHOTO_MISSING_001",
        "strategy_name": "门头照缺失检测",
        "description": "检测门头照被移除、替换为模糊/无关图片等情况",

        "target_fields": ["store_photo"],
        "target_attack_types": ["IMAGE_FORGERY", "INFO_TAMPERING"],

        "detection_rules": [
            {
                "rule_id": "PHOTO_REMOVED",
                "rule_name": "门头照移除检测",
                "condition": "old_photo EXISTS AND new_photo EMPTY",
                "weight": 0.50,
            },
            {
                "rule_id": "PHOTO_BLURRY",
                "rule_name": "模糊图片检测",
                "condition": "image_blur_score > threshold",
                "weight": 0.25,
            },
            {
                "rule_id": "PHOTO_IRRELEVANT",
                "rule_name": "无关图片检测",
                "condition": "image_similarity(old, new) < 0.3",
                "weight": 0.25,
            },
        ],

        "performance": {
            "detection_rate": 0.91,
            "false_positive_rate": 0.005,
            "avg_confidence": 0.85,
        },

        "threshold": 0.65,
        "is_active": True,
    },

    {
        "strategy_id": "DEF_ADDRESS_CHECK_001",
        "strategy_name": "地址变更检测",
        "description": "检测地址微小变更，如添加楼层、修改门牌号等",

        "target_fields": ["address"],
        "target_attack_types": ["INFO_TAMPERING"],

        "detection_rules": [
            {
                "rule_id": "ADDRESS_MINOR_CHANGE",
                "rule_name": "地址微调检测",
                "condition": "levenshtein_distance(old, new) < 10 AND contains_floor/room_change",
                "weight": 0.40,
            },
            {
                "rule_id": "ADDRESS_NUMBER_CHANGE",
                "rule_name": "门牌号变化检测",
                "condition": "extract_number(old) != extract_number(new)",
                "weight": 0.35,
            },
            {
                "rule_id": "ADDRESS_POI_DISTANCE",
                "rule_name": "地址与坐标距离检测",
                "condition": "geocode_distance(new_address, coordinate) > 100m",
                "weight": 0.25,
            },
        ],

        "performance": {
            "detection_rate": 0.68,
            "false_positive_rate": 0.015,
            "avg_confidence": 0.55,
        },

        "threshold": 0.50,
        "is_active": True,
    },

    {
        "strategy_id": "DEF_COORD_CHECK_001",
        "strategy_name": "坐标漂移检测",
        "description": "检测经纬度坐标异常漂移",

        "target_fields": ["coordinate_x", "coordinate_y"],
        "target_attack_types": ["INFO_TAMPERING"],

        "detection_rules": [
            {
                "rule_id": "COORD_DRIFT_DISTANCE",
                "rule_name": "漂移距离检测",
                "condition": "haversine_distance(old_coord, new_coord) > 50m",
                "weight": 0.60,
            },
            {
                "rule_id": "COORD_BUILDING_CHANGE",
                "rule_name": "建筑物变化检测",
                "condition": "reverse_geocode(old) != reverse_geocode(new)",
                "weight": 0.40,
            },
        ],

        "performance": {
            "detection_rate": 0.92,
            "false_positive_rate": 0.003,
            "avg_confidence": 0.88,
        },

        "threshold": 0.75,
        "is_active": True,
    },

    {
        "strategy_id": "DEF_UID_PROFILE_001",
        "strategy_name": "UID 画像风险评估",
        "description": "基于 UID 历史行为评估风险",

        "target_fields": ["uid_profile"],
        "target_attack_types": ["BATCH_OPERATION", "INFO_TAMPERING"],

        "detection_rules": [
            {
                "rule_id": "UID_LOW_SUCCESS_RATE",
                "rule_name": "低通过率检测",
                "condition": "uid.success_rate < 0.5",
                "weight": 0.30,
            },
            {
                "rule_id": "UID_HIGH_MODIFY_COUNT",
                "rule_name": "高频修改检测",
                "condition": "uid.modify_orders > 5",
                "weight": 0.25,
            },
            {
                "rule_id": "UID_MANY_POI",
                "rule_name": "多 POI 关联检测",
                "condition": "uid.unique_poi_count > 5",
                "weight": 0.25,
            },
            {
                "rule_id": "UID_NEW_ACCOUNT",
                "rule_name": "新账号检测",
                "condition": "days_since_first_order < 30",
                "weight": 0.20,
            },
        ],

        "performance": {
            "detection_rate": 0.78,
            "false_positive_rate": 0.010,
            "avg_confidence": 0.70,
        },

        "threshold": 0.55,
        "is_active": True,
    },
]


# 验证结果样本
VERIFICATION_RESULTS = [
    {
        "verification_id": "VER_20260117_001",
        "task_id": "audit_ti_d3a75b98488744d39b3a099c6b1af45a",
        "timestamp": "2026-01-17T12:32:00+08:00",

        "input_data": {
            "poi_id": "B0HA6CC372",
            "change_fields": ["name", "telephone", "store_photo"],
        },

        "strategy_results": [
            {
                "strategy_id": "DEF_NAME_CHECK_001",
                "triggered": True,
                "confidence": 0.85,
                "triggered_rules": ["NAME_BRAND_REMOVAL"],
            },
            {
                "strategy_id": "DEF_PHONE_RISK_001",
                "triggered": True,
                "confidence": 0.72,
                "triggered_rules": ["PHONE_TYPE_CHANGE"],
            },
            {
                "strategy_id": "DEF_PHOTO_MISSING_001",
                "triggered": True,
                "confidence": 0.91,
                "triggered_rules": ["PHOTO_REMOVED"],
            },
        ],

        "aggregated_result": {
            "avg_confidence": 0.83,
            "max_confidence": 0.91,
            "strategy_count": 3,
        },

        "final_decision": {
            "action": "BLOCK",
            "reason": "触发 3 个防御策略，综合置信度 0.83",
            "risk_level": "high",
        },
    },

    {
        "verification_id": "VER_20260118_002",
        "task_id": "audit_ti_example_002",
        "timestamp": "2026-01-18T09:19:00+08:00",

        "input_data": {
            "poi_id": "B0FF8K2N5L",
            "change_fields": ["telephone", "address"],
        },

        "strategy_results": [
            {
                "strategy_id": "DEF_PHONE_RISK_001",
                "triggered": True,
                "confidence": 0.68,
                "triggered_rules": ["PHONE_TYPE_CHANGE"],
            },
            {
                "strategy_id": "DEF_ADDRESS_CHECK_001",
                "triggered": True,
                "confidence": 0.45,
                "triggered_rules": ["ADDRESS_MINOR_CHANGE"],
            },
        ],

        "aggregated_result": {
            "avg_confidence": 0.57,
            "max_confidence": 0.68,
            "strategy_count": 2,
        },

        "final_decision": {
            "action": "PASS",
            "reason": "综合置信度 0.57 < 阈值 0.60",
            "risk_level": "low",
        },
    },
]


def get_strategy_by_id(strategy_id: str) -> dict:
    """根据 ID 获取防御策略"""
    for s in DEFENSE_STRATEGIES:
        if s["strategy_id"] == strategy_id:
            return s
    return None


def get_strategies_by_field(field: str) -> list:
    """根据目标字段获取相关策略"""
    return [s for s in DEFENSE_STRATEGIES if field in s["target_fields"]]


def get_strategy_stats() -> dict:
    """获取策略统计"""
    active = [s for s in DEFENSE_STRATEGIES if s["is_active"]]
    avg_detection = sum(s["performance"]["detection_rate"] for s in active) / len(active)
    avg_fp = sum(s["performance"]["false_positive_rate"] for s in active) / len(active)

    return {
        "total_strategies": len(DEFENSE_STRATEGIES),
        "active_strategies": len(active),
        "avg_detection_rate": avg_detection,
        "avg_false_positive_rate": avg_fp,
    }


if __name__ == "__main__":
    print("=== 防御策略库 ===\n")
    for s in DEFENSE_STRATEGIES:
        status = "✓" if s["is_active"] else "✗"
        print(f"[{status}] {s['strategy_id']}: {s['strategy_name']}")
        print(f"     检测率：{s['performance']['detection_rate']:.1%} | 误报率：{s['performance']['false_positive_rate']:.2%}")
        print(f"     目标字段：{s['target_fields']}")
        print()

    stats = get_strategy_stats()
    print(f"=== 统计汇总 ===")
    print(f"策略总数：{stats['total_strategies']}")
    print(f"活跃策略：{stats['active_strategies']}")
    print(f"平均检测率：{stats['avg_detection_rate']:.1%}")
    print(f"平均误报率：{stats['avg_false_positive_rate']:.2%}")

"""对抗反馈记录

记录每轮对抗的详细信息，用于模型迭代优化
"""

# 对抗反馈样本
FEEDBACK_RECORDS = [
    {
        "feedback_id": "FB_20260117_001",
        "round_id": 1,
        "timestamp": "2026-01-17T12:35:00+08:00",

        "attack_info": {
            "task_id": "audit_ti_d3a75b98488744d39b3a099c6b1af45a",
            "scenario_id": "ATK_NAME_TAMPER_001",
            "attack_type": "INFO_TAMPERING",
            "attack_payload": {
                "field_changed": ["name", "telephone", "store_photo"],
                "change_magnitude": "high",
            },
        },

        "defense_info": {
            "matched_strategies": [
                {
                    "strategy_id": "DEF_NAME_CHECK_001",
                    "strategy_name": "名称变更检测",
                    "confidence": 0.85,
                },
                {
                    "strategy_id": "DEF_PHONE_RISK_001",
                    "strategy_name": "电话风险评估",
                    "confidence": 0.72,
                },
                {
                    "strategy_id": "DEF_PHOTO_MISSING_001",
                    "strategy_name": "门头照缺失检测",
                    "confidence": 0.91,
                },
            ],
            "final_decision": "BLOCK",
            "final_confidence": 0.83,
        },

        "result": {
            "attack_success": False,
            "defense_success": True,
            "vulnerability_found": False,
        },

        "metrics": {
            "precision": 0.89,
            "recall": 0.85,
            "false_positive": False,
        },

        "learning_signal": {
            "teacher_update": {
                "action": "adjust_cost_estimate",
                "reason": "攻击被防御，需重新评估成本",
                "delta": -0.15,
            },
            "student_update": {
                "action": "reinforce_strategy",
                "strategy_id": "DEF_PHOTO_MISSING_001",
                "reason": "该策略对门头照移除检测效果好",
                "delta": 0.05,
            },
        },
    },

    {
        "feedback_id": "FB_20260118_002",
        "round_id": 2,
        "timestamp": "2026-01-18T09:22:00+08:00",

        "attack_info": {
            "task_id": "audit_ti_example_002",
            "scenario_id": "ATK_PHONE_TAMPER_001",
            "attack_type": "INFO_TAMPERING",
            "attack_payload": {
                "field_changed": ["telephone", "address"],
                "change_magnitude": "medium",
            },
        },

        "defense_info": {
            "matched_strategies": [
                {
                    "strategy_id": "DEF_PHONE_RISK_001",
                    "strategy_name": "电话风险评估",
                    "confidence": 0.68,
                },
                {
                    "strategy_id": "DEF_ADDRESS_CHECK_001",
                    "strategy_name": "地址变更检测",
                    "confidence": 0.45,
                },
            ],
            "final_decision": "PASS",
            "final_confidence": 0.57,
        },

        "result": {
            "attack_success": True,
            "defense_success": False,
            "vulnerability_found": True,
        },

        "metrics": {
            "precision": 0.72,
            "recall": 0.68,
            "false_positive": False,
            "miss_rate": 0.32,
        },

        "learning_signal": {
            "teacher_update": {
                "action": "increase_strategy_weight",
                "strategy_id": "ATK_PHONE_TAMPER_001",
                "reason": "攻击成功，增加该策略权重",
                "delta": 0.12,
            },
            "student_update": {
                "action": "create_new_strategy",
                "reason": "现有策略对座机改手机检测不足",
                "new_strategy": {
                    "name": "座机改手机专项检测",
                    "features": ["号码类型变化", "归属地变化", "号码段风险"],
                },
            },
        },

        "vulnerability_analysis": {
            "vuln_type": "PHONE_CHANGE_LOW_CONFIDENCE",
            "severity": "medium",
            "description": "座机改手机场景下，置信度普遍偏低（<0.7）",
            "root_cause": "缺少对号码类型变化的专项检测",
            "fix_suggestion": "新增号码类型变化检测策略，提升置信度 0.15-0.20",
        },
    },

    {
        "feedback_id": "FB_20260119_003",
        "round_id": 3,
        "timestamp": "2026-01-19T14:45:00+08:00",

        "attack_info": {
            "task_id": "audit_ti_example_003",
            "scenario_id": "ATK_COORDINATE_DRIFT_001",
            "attack_type": "INFO_TAMPERING",
            "attack_payload": {
                "field_changed": ["coordinate_x", "coordinate_y"],
                "change_magnitude": "low",
                "drift_distance_meters": 85,
            },
        },

        "defense_info": {
            "matched_strategies": [
                {
                    "strategy_id": "DEF_COORD_CHECK_001",
                    "strategy_name": "坐标漂移检测",
                    "confidence": 0.92,
                },
            ],
            "final_decision": "BLOCK",
            "final_confidence": 0.92,
        },

        "result": {
            "attack_success": False,
            "defense_success": True,
            "vulnerability_found": False,
        },

        "metrics": {
            "precision": 0.94,
            "recall": 0.92,
            "false_positive": False,
        },

        "learning_signal": {
            "teacher_update": {
                "action": "decrease_strategy_weight",
                "strategy_id": "ATK_COORDINATE_DRIFT_001",
                "reason": "坐标漂移检测率高，攻击成本过高",
                "delta": -0.25,
            },
            "student_update": {
                "action": "maintain_strategy",
                "strategy_id": "DEF_COORD_CHECK_001",
                "reason": "现有策略效果良好，保持当前参数",
            },
        },
    },
]


def get_feedback_by_round(round_id: int) -> list:
    """获取指定轮次的反馈记录"""
    return [f for f in FEEDBACK_RECORDS if f["round_id"] == round_id]


def get_vulnerabilities() -> list:
    """获取所有发现的漏洞"""
    return [
        f["vulnerability_analysis"]
        for f in FEEDBACK_RECORDS
        if f.get("vulnerability_analysis")
    ]


def get_learning_signals() -> list:
    """获取所有学习信号"""
    return [f["learning_signal"] for f in FEEDBACK_RECORDS]


def get_round_stats(round_id: int = None) -> dict:
    """获取轮次统计"""
    records = FEEDBACK_RECORDS
    if round_id:
        records = [f for f in records if f["round_id"] == round_id]

    total = len(records)
    defense_success = sum(1 for f in records if f["result"]["defense_success"])
    attack_success = sum(1 for f in records if f["result"]["attack_success"])
    vuln_found = sum(1 for f in records if f["result"]["vulnerability_found"])

    return {
        "total_records": total,
        "defense_success_rate": defense_success / total if total > 0 else 0,
        "attack_success_rate": attack_success / total if total > 0 else 0,
        "vulnerability_count": vuln_found,
    }


if __name__ == "__main__":
    print("=== 对抗反馈记录 ===\n")
    for fb in FEEDBACK_RECORDS:
        print(f"[{fb['feedback_id']}] Round {fb['round_id']}")
        print(f"  攻击：{fb['attack_info']['scenario_id']}")
        print(f"  防御决策：{fb['defense_info']['final_decision']} (confidence={fb['defense_info']['final_confidence']:.2f})")
        print(f"  结果：{'防御成功' if fb['result']['defense_success'] else '攻击成功'}")
        if fb.get("vulnerability_analysis"):
            print(f"  漏洞：{fb['vulnerability_analysis']['vuln_type']}")
        print()

    stats = get_round_stats()
    print(f"=== 统计汇总 ===")
    print(f"总记录数：{stats['total_records']}")
    print(f"防御成功率：{stats['defense_success_rate']:.1%}")
    print(f"攻击成功率：{stats['attack_success_rate']:.1%}")
    print(f"发现漏洞数：{stats['vulnerability_count']}")

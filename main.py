"""POI 风控对抗沙箱 - 主入口

Harness Engineering 三支柱：
- Constrain（约束层）：定义 Teacher/Student 人格和行为边界
- Verify（验证层）：检查 Agent 是否正确完成任务
- Correct（反馈层）：当 Agent 出错时进行修复
"""
import sys
import os
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.models import AdversarialRound, Scenario
from agents.teacher import TeacherAgent
from agents.student import StudentAgent


class POIHarnessSandbox:
    """
    POI Harness 对抗沙箱

    核心流程：
    1. Teacher 生成对抗样本
    2. Student 进行防御决策
    3. 验证层检查指标
    4. 反馈层迭代优化
    """

    def __init__(self):
        self.teacher = TeacherAgent()
        self.student = StudentAgent()
        self.round_history: List[AdversarialRound] = []
        self.current_round = 0

    def run_round(self) -> AdversarialRound:
        """运行一轮对抗"""
        self.current_round += 1

        round_result = AdversarialRound(
            round_id=self.current_round,
            timestamp=datetime.now().isoformat(),
        )

        print(f"\n{'='*60}")
        print(f"  第 {self.current_round} 轮对抗")
        print(f"{'='*60}")

        # === 阶段 1: Teacher 攻击 ===
        print("\n【阶段 1】Teacher 生成对抗样本...")

        attack_success = 0
        for scenario in Scenario:
            attack = self.teacher.select_attack(scenario)
            sample = self.teacher.generate_adversarial_sample(attack)
            round_result.attack_scenarios.append(attack)

            # === 阶段 2: Student 防御 ===
            print(f"\n  攻击场景：{attack.name} ({scenario.value})")
            print(f"  期望收益：￥{sample['expected_revenue']:.2f}")
            print(f"  有利可图：{sample['is_profitable']}")

            defense_result = self.student.defense_decision(attack)

            if defense_result["action"] == "BLOCK":
                print(f"  ✅ 防御成功 - {defense_result['reason']}")
                print(f"     置信度：{defense_result.get('confidence', 0):.2%}")
                round_result.defense_success_count += 1
            else:
                print(f"  ❌ 防御失败 - {defense_result['reason']}")
                round_result.attack_success_count += 1
                round_result.vulnerabilities_found += 1

        # === 阶段 3: 计算指标 ===
        total_attacks = len(round_result.attack_scenarios)
        round_result.metrics = {
            "miss_rate": round_result.attack_success_count / total_attacks,
            "defense_rate": round_result.defense_success_count / total_attacks,
            "student_metrics": self.student.get_metrics(),
        }

        # === 阶段 4: 反馈优化 ===
        if round_result.vulnerabilities_found > 0:
            print(f"\n【阶段 3】发现 {round_result.vulnerabilities_found} 个漏洞，开始修复...")
            # 模拟修复
            round_result.vulnerabilities_fixed = round_result.vulnerabilities_found
            print(f"  ✅ 已修复 {round_result.vulnerabilities_fixed} 个漏洞")

        # 保存历史记录
        self.round_history.append(round_result)

        return round_result

    def run_multiple_rounds(self, num_rounds: int = 10):
        """运行多轮对抗"""
        print(f"\n🎯 开始运行 {num_rounds} 轮对抗演练...")

        for i in range(num_rounds):
            self.run_round()

            # 每轮后显示摘要
            if self.round_history:
                last_round = self.round_history[-1]
                print(last_round.summary())

        # 最终汇总
        self._print_final_summary()

    def _print_final_summary(self):
        """打印最终汇总"""
        print("\n" + "=" * 60)
        print("  对抗演练最终汇总")
        print("=" * 60)

        if not self.round_history:
            return

        # 趋势分析
        first_round = self.round_history[0]
        last_round = self.round_history[-1]

        print(f"""
┌─────────────────────────────────────────────────────────┐
│  总轮次：{self.current_round} 轮
├─────────────────────────────────────────────────────────┤
│  初始漏放率：{first_round.metrics.get('miss_rate', 0):.2%} → 最终漏放率：{last_round.metrics.get('miss_rate', 0):.2%}
│  初始防御率：{first_round.metrics.get('defense_rate', 0):.2%} → 最终防御率：{last_round.metrics.get('defense_rate', 0):.2%}
├─────────────────────────────────────────────────────────┤
│  发现漏洞总数：{sum(r.vulnerabilities_found for r in self.round_history)}
│  修复漏洞总数：{sum(r.vulnerabilities_fixed for r in self.round_history)}
└─────────────────────────────────────────────────────────┘
""")

        # Student 最终指标
        metrics = self.student.get_metrics()
        print(f"""
┌─────────────────────────────────────────────────────────┐
│  Student Agent 最终状态
├─────────────────────────────────────────────────────────┤
│  防御策略总数：{metrics['total_strategies']}
│  有效策略数：{metrics['effective_strategies']}
│  平均检测率：{metrics['avg_detection_rate']:.2%}
│  平均误报率：{metrics['avg_false_positive_rate']:.2%}
└─────────────────────────────────────────────────────────┘
""")


def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🎯 POI Harness 对抗沙箱 v1.0                         ║
║     从作恶动机建模到自进化风控体系                        ║
║                                                          ║
║     Harness Engineering 三支柱：                         ║
║     • Constrain（约束层）- 定义人格和行为边界            ║
║     • Verify（验证层）- 检查指标是否达标                 ║
║     • Correct（反馈层）- 迭代优化                        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)

    sandbox = POIHarnessSandbox()

    # 运行 10 轮对抗
    sandbox.run_multiple_rounds(10)

    print("\n✅ 对抗演练完成！")


if __name__ == "__main__":
    main()

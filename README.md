# poi-agent

> Multi-Agent Adversarial Testing Framework for Content Risk Control

A harness engineering framework that uses Teacher/Student dual-agent adversarial training to discover vulnerabilities in content moderation systems and automatically iterate on defenses.

```
Teacher Agent (attacker) ──generates──→ Adversarial Samples
                                              │
                                              ▼
Student Agent (defender) ←──responds to─── Adversarial Samples
                                              │
                                              ▼
                                        Evaluate & Fix
                                              │
                                              ▼
                                   Iterate until convergence
```

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Install

```bash
git clone https://github.com/znxzsy/poi-agent.git
cd poi-agent
pip install graphviz  # for diagram generation
```

## Quick Start

```bash
python main.py
```

This runs 10 rounds of adversarial testing, where the Teacher Agent generates attack samples and the Student Agent attempts to defend against them.

## Architecture

### Three-Layer Harness

| Layer | Responsibility |
|-------|---------------|
| **Constrain** | Define Teacher/Student personality and behavioral boundaries |
| **Verify** | Check whether agent outputs meet quality thresholds |
| **Correct** | Fix issues and feed back into the next iteration |

### Components

```
poi-agent/
├── main.py             # Orchestration entry point
├── core/
│   └── models.py       # Data models: cost/revenue/risk/scenario
├── agents/
│   ├── teacher.py      # Teacher Agent (attacker side)
│   └── student.py      # Student Agent (defender side)
├── generate_diagrams.py  # Architecture diagram generator
└── website/            # Project site
```

## API Reference

### Core Models

**EvilCostModel** - Four-dimensional cost model:

```python
from core.models import EvilCostModel

cost = EvilCostModel(
    # Time cost (minutes)
    registration_time=10,
    operation_time=5,
    waiting_time=0,
    # Money cost (yuan)
    account_cost=0.1,
    device_cost=0,
    ip_cost=0,
    # Tech cost (1-10 difficulty)
    bypass_difficulty=2,
    tool_dev_cost=0,
    # Account cost
    ban_rate=0.3,
    reuse_count=10,
)

cost.total_time_cost()      # 15 minutes
cost.total_money_cost()     # 0.1 yuan
cost.tech_difficulty()      # 1.0
```

**EvilRevenue** - Expected revenue calculation:

```python
from core.models import EvilRevenue

revenue = EvilRevenue(
    success_revenue=10000,
    success_rate=0.7,
    failure_loss=1000,
    failure_rate=0.3,
)
revenue.expected_revenue()  # 6700.0
```

**AttackScenario** - Attack definition with cost/revenue/risk:

```python
from core.models import AttackScenario, AttackType, Scenario, EvilCostModel, EvilRevenue

attack = AttackScenario(
    name="AIGC 生成图",
    attack_type=AttackType.IMAGE_FORGERY,
    scenario=Scenario.UGC,
    description="Use Midjourney to generate fake store images",
    cost=EvilCostModel(operation_time=5, account_cost=0.1, bypass_difficulty=2),
    revenue=EvilRevenue(success_revenue=10000, success_rate=0.7),
)
attack.is_profitable()  # True/False based on cost-revenue analysis
```

**DefenseStrategy** - Defense capability with detection/false-positive rates:

```python
from core.models import DefenseStrategy, Scenario

strategy = DefenseStrategy(
    name="AIGC Detection",
    description="Detect AI-generated fake images",
    target_scenarios=[Scenario.GC],
    detection_rate=0.88,
    false_positive_rate=0.008,
)
strategy.is_effective()  # True if detection_rate >= 0.9 and fp_rate <= 0.01
```

### Agents

**TeacherAgent** - Generates adversarial samples:

```python
from agents.teacher import TeacherAgent
from core.models import Scenario

teacher = TeacherAgent()

# Select optimal attack (argmax(revenue - cost - risk))
best_attack = teacher.select_attack(scenario=Scenario.UGC)

# Generate adversarial sample details
sample = teacher.generate_adversarial_sample(best_attack)

# Evolve attack based on defense info
evolved = teacher.evolve_attack(best_attack, defense_info={"detected": True})
```

**StudentAgent** - Makes defense decisions:

```python
from agents.student import StudentAgent

student = StudentAgent()

# Defense decision for an attack
result = student.defense_decision(attack)
# Returns: {"action": "BLOCK"/"PASS", "confidence": 0.88, "strategies": [...]}

# Learn from a new attack
new_strategy = student.learn_from_attack(attack, result)

# Update strategy parameters
student.update_strategy("AIGC Detection", new_detection_rate=0.92, new_fp_rate=0.005)
```

### Orchestration

**POIHarnessSandbox** - Runs adversarial rounds:

```python
from main import POIHarnessSandbox

sandbox = POIHarnessSandbox()

# Run a single round
round_result = sandbox.run_round()

# Run multiple rounds
sandbox.run_multiple_rounds(num_rounds=10)
```

## Configuration

All attack scenarios and defense strategies are defined in their respective agent files (`agents/teacher.py`, `agents/student.py`). To customize:

1. **Add attack scenarios** - Append to `TeacherAgent.attack_scenarios` in `_init_attack_scenarios()`
2. **Add defense strategies** - Append to `StudentAgent.defense_strategies` in `_init_defense_strategies()`
3. **Adjust thresholds** - Modify `max_false_positive` in `DefenseStrategy` or the `threshold` in `StudentAgent.defense_decision()`

## Generate Diagrams

```bash
python generate_diagrams.py
```

Generates 4 professional diagrams to `docs/diagrams/`:
- System Architecture (4-layer: App/Agent/Core/Data)
- Cost Model (four-dimensional cost visualization)
- Adversarial Flow (4-phase adversarial process)
- Evolution Prediction (attack evolution timeline)

## License

MIT

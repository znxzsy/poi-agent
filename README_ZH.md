<p align="right"><a href="README.md">English</a> · <strong>中文</strong></p>

<p align="center">
  <img src="assets/hero.svg" alt="poi-agent 多智能体对抗评测框架" width="100%">
</p>

## 让防御策略经得住持续变化的测试

`poi-agent` 是一个轻量的多智能体对抗评测框架。Teacher 负责选择并演化测试场景，Student 负责执行防御策略，Harness 则保存每一轮证据、统计漏放与误判，并把失败样本带入下一轮测试。

这个项目面向受控实验、策略回归和研究验证，不用于对真实线上服务发起攻击。

<p align="center">
  <img src="docs/diagrams/adversarial_flow.png" alt="单轮对抗评测流程" width="96%">
</p>

## 这套框架解决什么问题

很多风控评测只能回答某个策略在固定数据上表现如何，却很难回答对手改变方式以后会怎样。`poi-agent` 把场景选择、防御决策、指标核验和失败回流放在同一条实验链路里，让每一次策略调整都有可比较的依据。

| 模块 | 作用 |
|---|---|
| **Teacher Agent** | 根据预期收益、执行成本和风险选择测试场景，并在反馈后调整场景。 |
| **Student Agent** | 调用已有防御策略，输出结构化的拦截或放行决定。 |
| **Harness Engine** | 约束智能体边界，核验指标，并记录纠正信息。 |
| **场景模型** | 显式表示成本、收益、风险、攻击类型和业务环境。 |
| **轮次记录** | 保存跨版本比较所需的实验数据与证据。 |

<p align="center">
  <img src="docs/diagrams/system_architecture.png" alt="poi-agent 系统架构" width="96%">
</p>

## 快速开始

```bash
git clone https://github.com/znxzsy/poi-agent.git
cd poi-agent
python main.py
```

运行测试：

```bash
python -m pytest tests -q
```

重新生成项目中的英文架构图：

```bash
pip install graphviz
python generate_diagrams.py
```

本机还需要安装 Graphviz 系统程序。

## 一轮评测如何运行

1. 按预期收益、成本与风险选择测试场景。
2. 生成结构化的对抗测试样本。
3. 由 Student 给出防御决策。
4. 统计防御率、漏放率和策略质量。
5. 保存失败证据，进入下一轮测试。

这样做的重点不是让智能体写出更漂亮的解释，而是让不同版本在同类场景上可以复现、比较和回归。

## 成本与风险建模

框架把时间、资金、技术难度、账号生命周期和风险拆开建模。场景为什么会被选中、策略为什么需要加强，都能落到明确字段和计算结果上，而不是藏在提示词里。

<p align="center">
  <img src="docs/diagrams/cost_model.png" alt="测试场景成本模型" width="92%">
</p>

## 项目结构

```text
poi-agent/
├── agents/             # Teacher 与 Student 策略
├── core/               # 场景、成本、收益和风险模型
├── feedback/           # 轮次反馈记录
├── scenarios/          # 场景定义
├── verification/       # 防御策略与核验逻辑
├── tests/              # 单元测试
├── docs/diagrams/      # 英文项目配图
├── generate_diagrams.py
└── main.py             # 实验编排入口
```

## 公开边界

公开仓库只包含研究演示与本地模拟，不包含生产凭证、内部数据、真实接口或可直接用于绕过线上系统的操作说明。它适合用来研究多智能体评测、反馈闭环和防御策略回归。

## 联系

研究合作或私有实现交流，请通过微信联系 **znxzsy**。

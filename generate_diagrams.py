"""Generate the English-only diagrams used by the public project pages."""

from pathlib import Path
import shutil

from graphviz import Digraph


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "docs/diagrams"
WEB_OUTPUT = ROOT / "website/docs"
OUTPUT.mkdir(parents=True, exist_ok=True)
WEB_OUTPUT.mkdir(parents=True, exist_ok=True)


def render(dot: Digraph, name: str) -> Path:
    path = Path(dot.render(str(OUTPUT / name), cleanup=True))
    shutil.copy2(path, WEB_OUTPUT / path.name)
    return path


def system_architecture() -> Path:
    dot = Digraph("system_architecture", format="png", engine="dot")
    dot.attr(rankdir="TB", size="22,16", dpi="300", bgcolor="white", fontname="Arial",
             label="POI-AGENT SYSTEM ARCHITECTURE\nHarness Engineering for Multi-Agent Adversarial Testing",
             labelloc="t", fontsize="20", fontcolor="#223247", pad="0.4", nodesep="0.6", ranksep="0.8")
    with dot.subgraph(name="cluster_app") as graph:
        graph.attr(label="APPLICATION LAYER", style="filled,rounded", fillcolor="#EDF4F8", color="#5D8FB6", penwidth="2")
        for node, label in (("cli", "CLI"), ("api", "API"), ("dashboard", "Evaluation dashboard")):
            graph.node(node, label, shape="box", style="filled,rounded", fillcolor="#5D8FB6", fontcolor="white")
    with dot.subgraph(name="cluster_agents") as graph:
        graph.attr(label="AGENT LAYER", style="filled,rounded", fillcolor="#F5F0F8", color="#9C79B5", penwidth="2")
        graph.node("teacher", "Teacher agent\nselects and evolves attacks", shape="box", style="filled,rounded", fillcolor="#B4564D", fontcolor="white")
        graph.node("student", "Student agent\napplies defense policies", shape="box", style="filled,rounded", fillcolor="#4C80AE", fontcolor="white")
        graph.node("evaluator", "Evaluator\ncomputes round metrics", shape="box", style="filled,rounded", fillcolor="#4D8B6B", fontcolor="white")
    with dot.subgraph(name="cluster_harness") as graph:
        graph.attr(label="HARNESS ENGINE", style="filled,rounded", fillcolor="#EEF7F1", color="#5A9875", penwidth="2")
        graph.node("constrain", "CONSTRAIN\nroles and boundaries", shape="box", style="filled,rounded", fillcolor="#5A9875", fontcolor="white")
        graph.node("verify", "VERIFY\nmetrics and thresholds", shape="box", style="filled,rounded", fillcolor="#5A9875", fontcolor="white")
        graph.node("correct", "CORRECT\nfeedback and policy updates", shape="box", style="filled,rounded", fillcolor="#5A9875", fontcolor="white")
    with dot.subgraph(name="cluster_data") as graph:
        graph.attr(label="DATA LAYER", style="filled,rounded", fillcolor="#FFF7EA", color="#C69243", penwidth="2")
        for node, label in (("scenarios", "Attack scenarios"), ("strategies", "Defense strategies"), ("history", "Round history"), ("metrics", "Metrics")):
            graph.node(node, label, shape="cylinder", style="filled", fillcolor="#E9C37D")
    dot.edges([("cli", "teacher"), ("api", "student"), ("dashboard", "evaluator")])
    dot.edge("teacher", "student", color="#B4564D", penwidth="3", label="attack")
    dot.edge("student", "teacher", color="#4C80AE", penwidth="2", style="dashed", label="defense", constraint="false")
    dot.edge("teacher", "constrain"); dot.edge("student", "constrain"); dot.edge("evaluator", "verify")
    dot.edge("constrain", "verify", color="#5A9875", penwidth="2"); dot.edge("verify", "correct", color="#5A9875", penwidth="2")
    for target in ("scenarios", "strategies", "history", "metrics"):
        dot.edge("correct", target, color="#C69243", style="dashed")
    return render(dot, "system_architecture")


def cost_model() -> Path:
    dot = Digraph("cost_model", format="png", engine="dot")
    dot.attr(rankdir="LR", size="18,10", dpi="300", bgcolor="white", fontname="Arial",
             label="ATTACK ECONOMICS MODEL\nRaise total attack cost above expected return",
             labelloc="t", fontsize="19", fontcolor="#223247", pad="0.4")
    dimensions = [
        ("time", "Time cost", "registration\noperation\nwaiting", "#B4564D"),
        ("money", "Financial cost", "accounts\ndevices\nnetwork", "#4C80AE"),
        ("technical", "Technical cost", "bypass difficulty\ntool development", "#C28A3B"),
        ("account", "Account cost", "ban rate\nreuse limit", "#8769A3"),
    ]
    for node, title, body, color in dimensions:
        dot.node(node, f"{title}\n\n{body}", shape="box", style="filled,rounded", fillcolor=color, fontcolor="white", width="2.2", height="1.5")
    dot.node("formula", "Expected return = success value × success rate − failure loss\n\nTotal cost = time + money + technical + account + risk",
             shape="note", style="filled", fillcolor="#F1F3F5", color="#8592A0", width="4.8", height="2")
    for node, *_ in dimensions:
        dot.edge(node, "formula", color="#667789", penwidth="2")
    return render(dot, "cost_model")


def adversarial_flow() -> Path:
    dot = Digraph("adversarial_flow", format="png", engine="dot")
    dot.attr(rankdir="LR", size="20,8", dpi="300", bgcolor="white", fontname="Arial",
             label="ADVERSARIAL TESTING ROUND", labelloc="t", fontsize="20", fontcolor="#223247", pad="0.4", nodesep="0.7")
    stages = [
        ("select", "1  Select attack\nmaximize return − cost − risk", "#B4564D"),
        ("generate", "2  Generate case\nmaterialize adversarial input", "#B4564D"),
        ("defend", "3  Apply defense\nBLOCK or PASS", "#4C80AE"),
        ("measure", "4  Measure\nrecall · miss rate · false positive", "#C28A3B"),
        ("update", "5  Update\nrepair policy and record evidence", "#4D8B6B"),
    ]
    for node, label, color in stages:
        dot.node(node, label, shape="box", style="filled,rounded", fillcolor=color, fontcolor="white", width="2.5", height="1.25")
    for left, right in zip(stages, stages[1:]):
        dot.edge(left[0], right[0], color="#607386", penwidth="3")
    dot.edge("update", "select", color="#4D8B6B", penwidth="2", style="dashed", label="next round", constraint="false")
    return render(dot, "adversarial_flow")


def evolution_prediction() -> Path:
    dot = Digraph("evolution_prediction", format="png", engine="dot")
    dot.attr(rankdir="LR", size="19,11", dpi="300", bgcolor="white", fontname="Arial",
             label="ATTACK EVOLUTION HYPOTHESES", labelloc="t", fontsize="20", fontcolor="#223247", pad="0.4", ranksep="0.8")
    columns = [
        ("observed", "Observed pattern", "#B4564D"),
        ("next", "Likely next step", "#C28A3B"),
        ("test", "Synthetic test", "#4C80AE"),
        ("response", "Defense response", "#4D8B6B"),
    ]
    rows = [
        ("Edited storefront image", "Generated storefront image", "Image provenance challenge", "Provenance + visual checks"),
        ("Scripted account abuse", "Agent-assisted abuse", "Coordination stress test", "Behavioral and graph signals"),
        ("Spliced video", "Generated video", "Temporal consistency case", "Frame and motion checks"),
    ]
    for col, title, color in columns:
        dot.node(f"head_{col}", title, shape="box", style="filled,rounded", fillcolor=color, fontcolor="white", width="2.3")
    for row_index, row in enumerate(rows):
        previous = None
        for col_index, (col, _, color) in enumerate(columns):
            node = f"r{row_index}_{col}"
            dot.node(node, row[col_index], shape="box", style="filled,rounded", fillcolor=f"{color}22", color=color, width="2.3", height="0.75")
            dot.edge(f"head_{col}", node, color=color, style="dotted", arrowhead="none")
            if previous:
                dot.edge(previous, node, color="#708090", penwidth="2")
            previous = node
    return render(dot, "evolution_prediction")


if __name__ == "__main__":
    for figure in (system_architecture, cost_model, adversarial_flow, evolution_prediction):
        print(figure())

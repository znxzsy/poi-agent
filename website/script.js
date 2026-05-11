// poi-agent website scripts

function runDemo(type) {
    const output = document.getElementById('terminal-output');
    const demos = {
        attack: `
<span class="prompt">$</span> TeacherAgent.select_attack(scenario=BGC)

▸ 选择最优攻击: argmax(收益 - 成本 - 风险)

  攻击: AIGC生成虚假门店照片
  成本模型:
    - 时间:    20 min/次
    - 资金:    ￥5/账号
    - 技术:    7/10
  期望收益: ￥2685.00
  有利可图: 是

  攻击: 多字段全面篡改
  成本模型:
    - 时间:    30 min/次
    - 资金:    ￥10/账号
    - 技术:    6/10
  期望收益: ￥1900.00
  有利可图: 是
`,
        defense: `
<span class="prompt">$</span> StudentAgent.defense_decision(attack)

▸ 匹配防御策略...

  攻击: AIGC生成虚假照片
  触发策略:
    + AIGC 图像检测         (检测率: 74%, FP: 1.8%)
    + 门头照缺失检测        (检测率: 91%, FP: 0.5%)
    + P 图篡改检测          (检测率: 71%, FP: 2.0%)

  最高置信度: 0.91
  决策: BLOCK

  攻击: 名称篡改-品牌蹭流
  触发策略:
    + 名称变更检测          (检测率: 85%, FP: 0.8%)
    + 多字段联合变更检测    (检测率: 83%, FP: 1.2%)

  最高置信度: 0.85
  决策: BLOCK
`,
        evolution: `
<span class="prompt">$</span> EvolutionEngine.generate_rl_transitions(feedback_records)

▸ 从 7 条对抗反馈生成 RL 样本...

  [✅ TP] ATK_NAME_TAMPER_001       | BLOCK | reward=+0.91
  [❌ FN] ATK_PHONE_TAMPER_001      | PASS  | reward=-2.55 ⚠️ 漏放
  [✅ TP] ATK_COORD_PRECISE_SHIFT   | BLOCK | reward=+0.92
  [✅ TP] ATK_PHOTO_AIGC_001        | BLOCK | reward=+0.71
  [✅ TP] ATK_PHOTO_AIGC_MERGE      | BLOCK | reward=+0.77
  [❌ FN] ATK_PHOTO_PHOTOSHOP_001   | PASS  | reward=-2.15 ⚠️ 漏放
  [✅ TP] ATK_ADDRESS_GEO_SPOOF     | BLOCK | reward=+0.85

▸ 策略梯度更新...
  image:   0.3000 → 0.2998 (梯度 +0.05)
  batch:   0.2494 → 0.2494 (未触发)
  tamper:  0.2512 → 0.2512 (梯度 +0.18)
  quality: 0.2000 → 0.1995 (未触发)

  样本: 7 | TP=5 FN=2 | avg_reward=-0.077
  数据集已导出: data/rl_training_data.json
`,
    };

    output.innerHTML = output.innerHTML + demos[type];
    output.scrollTop = output.scrollHeight;
}

// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// 导航栏滚动效果
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 10) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

console.log('%cpoi-agent v2.0', 'font-size: 20px; color: #c0392b; font-weight: bold;');
console.log('%c多智能体对抗沙箱', 'font-size: 14px; color: #5b8db8;');

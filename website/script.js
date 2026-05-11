// POI Harness 对抗沙箱 - 网站交互
function runDemo(type) {
    const output = document.getElementById('terminal-output');
    const demos = {
        attack: `
<span class="prompt">$</span> Teacher Agent - 攻击方

🔴 选择最优攻击方式...

  攻击场景：AIGC 生成图
  作恶成本:
    - 时间成本：5 分钟
    - 资金成本：￥0.1/张
    - 技术成本：低 (2/10)
  期望收益：￥7000.00
  是否有利可图：✅ 是

  攻击场景：UID 批量刷单
  作恶成本:
    - 时间成本：12 分钟/账号
    - 资金成本：￥5/账号
    - 账号成本：封号率 30%
  期望收益：￥29600.00
  是否有利可图：✅ 是
`,
        defense: `
<span class="prompt">$</span> Student Agent - 防御方

🔵 收到攻击：AIGC 生成图

  匹配防御策略:
    ✅ AIGC 检测 (检测率 88%)
    ✅ 图像真伪检测 (检测率 92%)
    ✅ 互联网发现 (检测率 85%)

  综合置信度：88.5%
  决策： BLOCK (拦截)

  匹配防御策略:
    ✅ UID 关联分析 (检测率 95%)
    ✅ 设备指纹识别 (检测率 93%)

  综合置信度：94.0%
  决策：🚫 BLOCK (拦截)
`,
        result: `
<span class="prompt">$</span> 第 1 轮对抗结果

┌─────────────────────────────────────────────┐
│  攻击成功：0 | 防御成功：8                  │
│  发现漏洞：0 | 修复漏洞：0                  │
│  漏放率：0.00% | 误拦率：0.50%             │
└─────────────────────────────────────────────┘

 防御指标:
  - 防御策略总数：12
  - 有效策略数：11
  - 平均检测率：91.5%
  - 平均误报率：0.58%

✅ 对抗演练完成！
`
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
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(26, 26, 46, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
    } else {
        navbar.style.background = 'var(--dark)';
    }
});

console.log('%c🎯 POI Harness 对抗沙箱 v1.0', 'font-size: 20px; color: #E74C3C;');
console.log('%c从作恶动机建模到自进化风控体系', 'font-size: 14px; color: #3498DB;');
console.log('GitHub: https://github.com/znxzsy/poi-agent');

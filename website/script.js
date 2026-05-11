function runDemo(type) {
    const output = document.getElementById('terminal-output');
    const demos = {
        attack: `
<span class="prompt">$</span> TeacherAgent.select_attack(scenario=UGC)

Selecting optimal attack (argmax(revenue - cost - risk))...

  Attack: AIGC Generated Image
  Cost Model:
    - Time:       5 min
    - Money:      ￥0.10/image
    - Tech:       2/10
  Expected Revenue: ￥7000.00
  Profitable: Yes

  Attack: UID Batch Operations
  Cost Model:
    - Time:       12 min/account
    - Money:      ￥5/account
    - Account:    30% ban rate
  Expected Revenue: ￥29600.00
  Profitable: Yes
`,
        defense: `
<span class="prompt">$</span> StudentAgent.defense_decision(attack)

Matching defense strategies...

  Attack: AIGC Generated Image
  Strategies matched:
    + AIGC Detection       (detection: 88%, FP: 0.8%)
    + Image Verification   (detection: 92%, FP: 0.5%)
    + Internet Discovery   (detection: 85%, FP: 1.0%)

  Combined confidence: 88.5%
  Decision: BLOCK

  Attack: UID Batch Operations
  Strategies matched:
    + UID Correlation      (detection: 95%, FP: 0.3%)
    + Device Fingerprint   (detection: 93%, FP: 0.5%)

  Combined confidence: 94.0%
  Decision: BLOCK
`,
        result: `
<span class="prompt">$</span> Round 1 Complete

┌─────────────────────────────────────────┐
│  Attacks blocked: 2 | Passed: 6         │
│  Vulnerabilities found: 0 | Fixed: 0   │
│  Miss rate: 0.00% | FP rate: 0.50%    │
└─────────────────────────────────────────┐

Student Metrics:
  Total strategies:     12
  Effective strategies: 11
  Avg detection rate:   91.5%
  Avg false positive:   0.58%
`
    };

    output.innerHTML = output.innerHTML + demos[type];
    output.scrollTop = output.scrollHeight;
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(26, 26, 46, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
    } else {
        navbar.style.background = 'var(--dark)';
    }
});

console.log('%.poi-agent v1.0', 'font-size: 20px; color: #E74C3C;');
console.log('%cMulti-Agent Adversarial Testing Framework', 'font-size: 14px; color: #3498DB;');

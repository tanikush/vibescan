import re
from pathlib import Path
from vibescan.rules.secrets import SECRET_PATTERNS
from vibescan.rules.vibe_patterns import VIBE_PATTERNS
from vibescan.rules.ai_risk_patterns import AI_RISK_PATTERNS
from vibescan.rules.entropy import find_high_entropy_strings

content = Path('tests/fixtures/vulnerable_app.py').read_text()
lines = content.splitlines()

ALL_PATTERNS = [
    *[(name, pat, risk) for name, pat, risk, *desc in SECRET_PATTERNS],
    *[(name, pat, risk) for name, pat, risk, desc in VIBE_PATTERNS],
    *[(name, pat, risk, _) for name, pat, risk, _ in AI_RISK_PATTERNS],
]

found = set()
for pname, regex, risk, *desc in ALL_PATTERNS:
    for i, line in enumerate(lines, 1):
        if re.search(regex, line):
            found.add(pname)

found_entropy = set()
for secret, score in find_high_entropy_strings(content):
    if score > 4.5:
        found_entropy.add(f'High Entropy ({secret[:30]})')

EXPECTED = {
    'AWS Access Key', 'AWS Secret Key', 'Database URL',
    'Dangerous eval()', 'Subprocess shell=True', 'YAML Unsafe Load',
    'Debug Mode Enabled', 'Missing Auth Check', 'Weak Random for Security',
    'Password Logged',
}

print('=== EXPECTED vs ACTUAL ===')
for ex in sorted(EXPECTED):
    status = 'OK  ' if ex in found else 'MISS'
    print(f'  [{status}] {ex}')

print(f'\nEntropy findings: {len(found_entropy)}')
for s in sorted(found_entropy):
    print(f'  {s}')

total = len(found) + len(found_entropy)
print(f'\nTotal detected: {total}')
print(f'\nGitHub access key sub-proj fix: \"sk-[a-zA-Z0-9_-]{{20,}}\" matches?', end=' ')
m = re.search(r'sk-[a-zA-Z0-9_-]{20,}', content)
print(m.group()[:60] if m else 'NO')

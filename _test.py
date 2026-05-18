import re
text = 'OPENAI_KEY = "sk-proj-abcdefghijklmnopqrstuvwxyz1234567890ABCDEF"'
patterns = [
    ('old-48', r'sk-[a-zA-Z0-9]{48}'),
    ('new-flexible', r'sk-[a-zA-Z0-9_-]{20,}'),
    ('openai-proj', r'sk-(?:proj-)?[a-zA-Z0-9]{48,}'),
]
for name, pat in patterns:
    m = re.search(pat, text)
    print(f'{name}: {m.group()[:60] if m else "NO MATCH"}')

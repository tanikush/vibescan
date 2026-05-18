from typing import Dict, Tuple, Optional


FIX_DATABASE: Dict[str, Tuple[str, str]] = {
    'AWS Access Key': (
        'Move to environment variable - do not hardcode in code.',
        '# BAD:\naws_key = "AKIAIOSFODNN7EXAMPLE"\n\n# GOOD:\nimport os\naws_key = os.getenv("AWS_ACCESS_KEY_ID")'
    ),
    'OpenAI API Key': (
        'Use OPENAI_API_KEY environment variable.',
        '# BAD:\nclient = OpenAI(api_key="sk-abc123...")\n\n# GOOD:\nimport os\nclient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))'
    ),
    'Database URL': (
        'Store in DATABASE_URL environment variable.',
        '# BAD:\ndb = "postgresql://user:pass@localhost/db"\n\n# GOOD:\nimport os\ndb = os.getenv("DATABASE_URL")'
    ),
    'SQL Injection Risk': (
        'Use parameterized queries instead of f-strings.',
        '# BAD:\nquery = f"SELECT * FROM users WHERE id = {user_id}"\n\n# GOOD:\nquery = "SELECT * FROM users WHERE id = ?"\ncursor.execute(query, (user_id,))'
    ),
    'Debug Mode Enabled': (
        'Set DEBUG=False in production. Control via .env.',
        '# BAD:\napp.run(debug=True)\n\n# GOOD:\nimport os\ndebug = os.getenv("DEBUG", "False").lower() == "true"\napp.run(debug=debug)'
    ),
    'CORS Wildcard': (
        'Use specific origins instead of wildcard.',
        '# BAD:\nCORS(app, origins="*")\n\n# GOOD:\nimport os\nallowed = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",\nCORS(app, origins=allowed)'
    ),
    'Dangerous eval()': (
        'Remove eval() - use json.loads or ast.literal_eval.',
        '# BAD:\nresult = eval(user_input)\n\n# GOOD (JSON):\nimport json\nresult = json.loads(user_input)\n\n# GOOD (Python literals):\nimport ast\nresult = ast.literal_eval(user_input)'
    ),
    'Missing Auth Check': (
        'Add authentication decorator to every API endpoint.',
        '# BAD:\ndef get_user(id): return db.get(id)\n\n# GOOD (Flask):\n@app.route("/user/<id>")\n@require_auth\ndef get_user(id): return db.get(id)'
    ),
    'YAML Unsafe Load': (
        'Use yaml.safe_load() instead of yaml.load().',
        '# BAD:\ndata = yaml.load(content)\n\n# GOOD:\ndata = yaml.safe_load(content)'
    ),
    'Unsafe subprocess': (
        'Use shell=False and validate inputs.',
        '# BAD:\nsubprocess.run(cmd, shell=True)\n\n# GOOD:\nsubprocess.run(["cmd", arg1, arg2], shell=False)'
    ),
}


def get_fix(pattern_name: str) -> Optional[Tuple[str, str]]:
    if pattern_name in FIX_DATABASE:
        return FIX_DATABASE[pattern_name]
    for key in FIX_DATABASE:
        if key.lower() in pattern_name.lower():
            return FIX_DATABASE[key]
    return None
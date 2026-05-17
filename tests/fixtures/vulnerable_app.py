# tests/fixtures/vulnerable_app.py
# INTENTIONALLY VULNERABLE — For Demo and Testing ONLY
# DO NOT use this code in real projects

import os
import sqlite3
import yaml
import subprocess
import random

# CRITICAL: Hardcoded AWS credentials
AWS_KEY = 'AKIAIOSFODNN7EXAMPLE'
AWS_SECRET = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'

# CRITICAL: Hardcoded OpenAI API key
OPENAI_KEY = 'sk-proj-abcdefghijklmnopqrstuvwxyz1234567890ABCDEF'

# CRITICAL: Database URL with password
DB_URL = 'postgresql://admin:password123@localhost:5432/myapp'

# HIGH: Debug mode enabled
DEBUG = True

# CRITICAL: SQL Injection vulnerability
def get_user(user_id):
    conn = sqlite3.connect('app.db')
    query = f'SELECT * FROM users WHERE id = {user_id}'
    return conn.execute(query).fetchone()

# HIGH: Password logged in plaintext
def login(username, password):
    print(f'Login attempt: {username} / {password}')
    pass

# CRITICAL: Dangerous eval() usage
def calculate(expression):
    return eval(expression)

# CRITICAL: Shell injection via shell=True
def run_cmd(cmd):
    subprocess.run(cmd, shell=True)

# CRITICAL: Unsafe YAML loading
def load_config(data):
    return yaml.load(data)

# HIGH: Weak random for security tokens
def gen_token():
    token = str(random.random())
    return token

# DEMO — intentionally vulnerable app for GIF recording
import os, sqlite3, yaml, subprocess, random

# CRITICAL — hardcoded secrets
AWS_KEY    = 'AKIAIOSFODNN7EXAMPLE'
AWS_SECRET = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
OPENAI_KEY = 'sk-proj-abcdefghijklmnopqrstuvwxyz1234567890ABCDEF'
DB_URL     = 'postgresql://admin:password123@localhost:5432/myapp'

# HIGH — debug on
DEBUG = True

# CRITICAL — SQL injection
def get_user(user_id):
    conn = sqlite3.connect('app.db')
    query = f'SELECT * FROM users WHERE id = {user_id}'
    return conn.execute(query).fetchone()

# HIGH — password in log
def login(username, password):
    print(f'Login: {username} / {password}')

# CRITICAL — eval()
def calculate(expression):
    return eval(expression)

# CRITICAL — shell=True
def run_cmd(cmd):
    subprocess.run(cmd, shell=True)

# CRITICAL — yaml.load()
def load_config(data):
    return yaml.load(data)

# HIGH — random module
def gen_token():
    return str(random.random())

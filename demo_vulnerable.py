# Demo file showing VibeScan detection capabilities
# This file contains INTENTIONALLY vulnerable code for demonstration

# CRITICAL: Hardcoded AWS credentials
AWS_KEY = "AKIAIOSFODNN7EXAMPLE"

# CRITICAL: Database URL with password
DATABASE_URL = "postgresql://admin:secret123@localhost:5432/myapp"

# HIGH: Debug mode enabled in production
DEBUG = True

# HIGH: SQL injection vulnerability
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL Injection
    return query

# CRITICAL: Dangerous eval()
def calculate(expr):
    return eval(expr)  # Code injection risk

print("Demo scan complete")
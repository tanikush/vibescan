import re

# Secret detection patterns - (name, regex, risk_level)
SECRET_PATTERNS = [
    # AWS Keys
    ('AWS Access Key', r'AKIA[0-9A-Z]{16}', 'CRITICAL'),
    ('AWS Secret Key', r'(?i)aws.{0,20}[\'"][0-9a-zA-Z/+]{40}[\'"]', 'CRITICAL'),
    
    # OpenAI
    ('OpenAI API Key', r'sk-[a-zA-Z0-9_-]{20,}', 'CRITICAL'),
    
    # GitHub
    ('GitHub Token', r'ghp_[a-zA-Z0-9]{36}', 'HIGH'),
    ('GitHub OAuth', r'gho_[a-zA-Z0-9]{36}', 'HIGH'),
    ('GitHub PAT', r'github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}', 'HIGH'),
    
    # Google / Firebase
    ('Google API Key', r'AIza[0-9A-Za-z\-_]{35}', 'HIGH'),
    
    # JWT Tokens
    ('JWT Token', r'eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*', 'HIGH'),
    
    # Database URLs
    ('Database URL', r'(?i)(mongodb|postgresql|mysql|redis)://[^\s<>"]+', 'CRITICAL'),
    
    # Generic Secrets
    ('Generic API Key', r'(?i)(api_key|apikey|api-key)\s*[=:]\s*[\'"][a-zA-Z0-9_\-]{20,}[\'"]', 'HIGH'),
    ('Generic Password', r'(?i)(password|passwd|pwd)\s*[=:]\s*[\'"][^\'"]{8,}[\'"]', 'MEDIUM'),
    ('Private Key', r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', 'CRITICAL'),
    
    # Stripe
    ('Stripe Secret Key', r'sk_live_[0-9a-zA-Z]{24}', 'CRITICAL'),
    ('Stripe Test Key', r'sk_test_[0-9a-zA-Z]{24}', 'HIGH'),
    
    # Slack
    ('Slack Token', r'xox[baprs]-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{24}', 'HIGH'),
    
    # .env file
    ('Hardcoded .env Value', r'(?m)^(?!#)[A-Z_]+=.{8,}$', 'MEDIUM'),
]

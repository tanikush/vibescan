# AI-generated code specific vulnerability patterns
VIBE_PATTERNS = [
    # Missing Authentication
    ('Missing Auth Check',
     r'(?i)def\s+(get|post|put|delete)_[a-z]+\s*\([^)]*\)(?!.*auth)',
     'HIGH',
     'AI often forgets authentication checks in API endpoints'),
    
    # SQL Injection
    ('SQL Injection Risk',
     r'(?i)(execute|query)\s*\(.*[f\'"].*{.*}.*[f\'"]',
     'CRITICAL',
     'Using f-strings directly in SQL queries creates injection risk'),
    
    # Hardcoded Credentials
    ('Hardcoded Admin Password',
     r'(?i)(admin|root|test).*[:=].*[\'\"](admin|password|123456|root)[\'"]',
     'CRITICAL',
     'Default credentials - AI commonly adds these'),
    
    # Debug Mode in Production
    ('Debug Mode Enabled',
     r'(?i)debug\s*=\s*True',
     'HIGH',
     'Debug=True in production exposes stack traces'),
    
    # CORS Wildcard
    ('CORS Wildcard',
     r'(?i)allow_origins.*\*|Access-Control-Allow-Origin.*\*',
     'HIGH',
     'Wildcard CORS allows API access from any origin'),
    
    # Exposed .env
    ('Direct .env Read',
     r'open\s*\(.*\.env.*\)',
     'MEDIUM',
     'Use python-dotenv instead of directly reading .env files'),
    
    # eval() Usage
    ('Dangerous eval()',
     r'\beval\s*\(',
     'CRITICAL',
     'eval() can execute arbitrary code'),
    
    # Pickle Usage
    ('Unsafe Pickle',
     r'pickle\.loads\s*\(',
     'HIGH',
     'pickle.loads on untrusted data creates RCE risk'),
]

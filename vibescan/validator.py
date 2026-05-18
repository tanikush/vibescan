import requests
from enum import Enum
from typing import Optional


class ValidityStatus(Enum):
    LIVE = 'LIVE'
    REVOKED = 'REVOKED'
    UNKNOWN = 'UNKNOWN'
    ERROR = 'ERROR'


TIMEOUT = 5


def check_github_token(token: str) -> ValidityStatus:
    try:
        r = requests.get('https://api.github.com/user',
                        headers={'Authorization': f'token {token}'},
                        timeout=TIMEOUT)
        if r.status_code == 200:
            return ValidityStatus.LIVE
        if r.status_code == 401:
            return ValidityStatus.REVOKED
        return ValidityStatus.UNKNOWN
    except requests.RequestException:
        return ValidityStatus.ERROR


def check_openai_key(api_key: str) -> ValidityStatus:
    try:
        r = requests.get('https://api.openai.com/v1/models',
                        headers={'Authorization': f'Bearer {api_key}'},
                        timeout=TIMEOUT)
        if r.status_code == 200:
            return ValidityStatus.LIVE
        if r.status_code == 401:
            return ValidityStatus.REVOKED
        if r.status_code == 429:
            return ValidityStatus.LIVE
        return ValidityStatus.UNKNOWN
    except requests.RequestException:
        return ValidityStatus.ERROR


def verify_finding(pattern_name: str, matched_text: str) -> ValidityStatus:
    t = matched_text.strip()
    n = pattern_name.lower()
    if 'github' in n and t.startswith(('ghp_', 'gho_', 'github_pat_')):
        return check_github_token(t)
    if 'openai' in n and t.startswith('sk-'):
        return check_openai_key(t)
    return ValidityStatus.UNKNOWN
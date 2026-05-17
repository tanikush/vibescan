import math
import re
from typing import List, Tuple

BASE64_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
HEX_CHARS = '0123456789abcdefABCDEF'

def shannon_entropy(data: str, charset: str) -> float:
    '''
    Calculate Shannon Entropy for a given string.
    Score ranges from 0.0 to 5.0+
    4.5+ indicates very likely a secret
    '''
    if not data:
        return 0.0
    
    filtered = [c for c in data if c in charset]
    if not filtered:
        return 0.0
    
    freq = {}
    for c in filtered:
        freq[c] = freq.get(c, 0) + 1
    
    length = len(filtered)
    entropy = 0.0
    for count in freq.values():
        prob = count / length
        entropy -= prob * math.log2(prob)
    
    return entropy

def find_high_entropy_strings(content: str, min_length: int = 20, threshold: float = 4.5) -> List[Tuple[str, float]]:
    '''
    Find high-entropy strings in file content.
    Returns: list of (string, entropy_score) tuples
    '''
    findings = []
    
    # Search for Base64 strings
    b64_pattern = r'[A-Za-z0-9+/=]{' + str(min_length) + r',}'
    for match in re.finditer(b64_pattern, content):
        s = match.group()
        score = shannon_entropy(s, BASE64_CHARS)
        if score > threshold:
            findings.append((s, score))
    
    # Search for Hex strings
    hex_pattern = r'[0-9a-fA-F]{' + str(min_length) + r',}'
    for match in re.finditer(hex_pattern, content):
        s = match.group()
        score = shannon_entropy(s, HEX_CHARS)
        if score > threshold:
            findings.append((s, score))
    
    return findings

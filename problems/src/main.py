import re
import unicodedata
from collections import Counter

def sanitize_user_inputs(inputs: list[str]) -> dict:
    cleaned = []
    threats = Counter()

    xss_pattern = re.compile(r'<.*?>|script', re.IGNORECASE)
    sqli_pattern = re.compile(r"('|--|;|/\*|drop|select|insert|or\s+1=1)", re.IGNORECASE)
    cmd_pattern = re.compile(r'[;&|`]|(\$\(.*\))|(\.\./)', re.IGNORECASE)

    for raw in inputs:
        normalized = unicodedata.normalize('NFKD', raw).encode('ascii', 'ignore').decode()
        sanitized = re.sub(r"[<>\"'`;]", "", normalized)
        sanitized = re.sub(r"script", "", sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r"\$\([^)]+\)", "", sanitized)

        # Detect threats
        if xss_pattern.search(raw):
            threats['xss'] += 1
        if sqli_pattern.search(raw):
            threats['sqli'] += 1
        if cmd_pattern.search(raw):
            threats['cmd_injection'] += 1

        cleaned.append(sanitized)

    return {
        "cleaned_inputs": cleaned,
        "threats_detected": dict(threats)
    }

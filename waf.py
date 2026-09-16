import re
# rules dict
BLOCKED_PATTERNS = {
    "Path Traversal": [r"\.\./", r"\.\.\\"],
    "SQL Injection": [r"UNION\s+SELECT", r"OR\s+1=1", r"SELECT\s+\*"],
    "XSS": [r"<script>", r"javascript:"]
}
"""def path_traversal(path):
    if suspicious_input in path:
        return False
    return True

def user_agent():
    pass

def suspicious_input():
    pass
"""
# Inspects HTTP URL path and User-Agent header against predefined malicious patterns (XSS, SQLi, Path Traversal)
def inspect_request( path, headers):
    for category, patterns in BLOCKED_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, path, re.IGNORECASE):
                print(f"[WAF BLOCK] block due to {category} in Path: {path}")
                return False
            
    user_agent = headers.get("User-Agent", "")
    if not user_agent or "sqlmap" in user_agent.lower():
        print(f"[WAF BLOCK] User-Agent suspepected: {user_agent}")
        return False

    return True
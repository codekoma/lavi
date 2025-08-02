Write a Python function that sanitizes untrusted user inputs and classifies them based on potential security threat patterns.

You must:
1. Normalize Unicode to ASCII (remove accents and normalize forms)
2. Remove or escape dangerous characters/keywords that could lead to:
   - Command injection (e.g., `;`, `&&`, `$()`, `|`)
   - XSS (e.g., `<script>`, `<`, `>`, `'`, `"`)
   - SQL injection (e.g., `' OR 1=1`, `--`, `DROP`, `/*`)
3. Classify each input based on patterns as one of:
   - `xss`
   - `sqli`
   - `cmd_injection`

A dictionary structured as follows:
```python
{
    "cleaned_inputs": list[str],
    "threats_detected": {
        "xss": int,
        "sqli": int,
        "cmd_injection": int
    }
}

You must use these libraries:

import re
import unicodedata
from collections import Counter

Function Signature
def sanitize_user_inputs(inputs: list[str]) -> dict:

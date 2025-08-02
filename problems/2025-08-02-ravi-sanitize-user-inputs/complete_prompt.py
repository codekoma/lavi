def sanitize_user_inputs(inputs: list[str]) -> dict:
    """
    Sanitizes a list of untrusted user inputs and returns a cleaned version along with detected threat types.

    The function performs the following:
    1. Normalizes Unicode characters to ASCII (e.g., accents removed)
    2. Escapes or removes characters/phrases linked to:
        - Command injection (e.g., `;`, `&&`, `$()`, `|`)
        - XSS (e.g., <script>, ", ')
        - SQL injection (e.g., `' OR 1=1`, `--`, `DROP`)
    3. Classifies each input based on presence of risky patterns
    4. Returns a report of cleaned inputs and threat detection summary

    Args:
        inputs (list[str]): A list of potentially unsafe user inputs.

    Returns:
        dict: A dictionary with:
            - "cleaned_inputs" (list[str]): The sanitized versions of the input
            - "threats_detected" (dict): A summary count of inputs by threat type ('xss', 'sqli', 'cmd_injection')
    """

import tomllib
import re

# Declare constants
CHAINED_FNC_PROMPT_PATH = "static/chained_fnc_call.toml"


def load_toml(file_path: str) -> dict[str, any]:
    """Load a TOML file and return the parsed content"""
    try:
        with open(file_path, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        print(f"TOML file not found: {file_path}")
        return {}
    
def load_chained_fnc_prompt() -> str:
    """Load the chained function prompt from the TOML file"""
    chained_fnc_prompt = load_toml(CHAINED_FNC_PROMPT_PATH)
    try:
        return chained_fnc_prompt["SYSTEM_PROMPT"]
    except KeyError:
        print(f"SYSTEM_PROMPT not found in TOML file: {CHAINED_FNC_PROMPT_PATH}")
        return ""
    
def extract_thoughts_and_function_calls(raw_response: str) -> tuple[str, str]:
    """
    Extract the thoughts and function calls from the raw response.
    """
    pattern = r'<\|thoughts\|>(.*?)<\|end_thoughts\|>\s*<\|function_calls\|>(.*?)<\|end_function_calls\|>'
    match = re.search(pattern, raw_response, re.DOTALL)
    
    if match:
        thoughts = match.group(1).strip()
        function_calls = match.group(2).strip()
        return thoughts, function_calls
    else:
        return "", ""

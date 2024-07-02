import tomllib
from os.path import join

from jinja2 import Environment, FileSystemLoader

from src.schemas import FunctionMetadata

# Declare constants
CHAINED_FNC_PROMPT_PATH = "static/chained_fnc_call.toml"
FNC_TEMPLATE_PATH = "chained_fnc_call.j2"

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(join("static", "templates")))

def load_toml(file_path: str) -> dict[str, any]:
    """Load a TOML file and return the parsed content"""
    try:
        with open(file_path, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        print(f"TOML file not found: {file_path}")
        return {}
    
def load_fnc_template(
        template_name: str = FNC_TEMPLATE_PATH,
        fnc_metadata: FunctionMetadata = None
    ) -> str:
    """Load the function template from the Jinja2 template file"""
    template = env.get_template(template_name)
    
    if fnc_metadata:
        return template.render(functions_metadata=fnc_metadata)
    else:
        print("No function metadata provided. Rendering an empty template.")
        return template.render(functions_metadata=[])
    
def load_chained_fnc_prompt() -> str:
    """Load the chained function prompt from the TOML file"""
    chained_fnc_prompt = load_toml(CHAINED_FNC_PROMPT_PATH)
    try:
        return chained_fnc_prompt["SYSTEM_PROMPT"]
    except KeyError:
        print(f"SYSTEM_PROMPT not found in TOML file: {CHAINED_FNC_PROMPT_PATH}")
        return ""
from os.path import join

from jinja2 import Environment, FileSystemLoader

from src.schemas import FunctionsMetadata
from src.settings import STATIC_DIR, FN_CALL_TEMPLATE_PATH, FN_GENERATE_TEMPLATE_PATH

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(join(STATIC_DIR, "templates")))

def load_jinja_template(template_name: str, context: dict[str, any]) -> str:
    """Load a Jinja2 template and render it with the given context"""
    template = env.get_template(template_name)
    return template.render(context)
    
def load_fn_call_template(
        template_name: str = FN_CALL_TEMPLATE_PATH,
        fnc_metadata: FunctionsMetadata = None
    ) -> str:
    """Load the function template from the Jinja2 template file"""
    context = {"functions_metadata": fnc_metadata} if fnc_metadata else {"functions_metadata": []}
    return load_jinja_template(template_name, context)

def load_fn_generate_template(
        template_name: str = FN_GENERATE_TEMPLATE_PATH,
        category: str = None,
        subcategory: str = None,
        tasks: list[str] = []
    ) -> str:
    """Load the function generation template from the Jinja2 template file"""
    context = {"category": category, "subcategory": subcategory, "tasks": tasks}
    return load_jinja_template(template_name, context)
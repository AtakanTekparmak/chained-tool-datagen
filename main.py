import argparse
from dotenv import load_dotenv

from src.models import construct_model      
from src.schemas import ChainedFNCResponse, FunctionsMetadata
from src.models.config import ModelConfig
from src.templates import load_fn_call_template
from src.components.function_schema_generator import generate_function_schemas

from easy_fnc.function_caller import FunctionCallingEngine, create_functions_metadata

def function_calling_flow():
    # Load the .env file
    load_dotenv()

    # Load the function call template
    fnc_metadata = create_functions_metadata(file_path="static/sample_functions.py")
    fn_call_template = load_fn_call_template(
        fnc_metadata=FunctionsMetadata.from_list(fnc_metadata)
    )
    
    # Create a ModelConfig instance
    model_config = ModelConfig(
        client="groq",
        system_prompt=fn_call_template,
        temperature=0.5,
        fewshot_examples=None
    )
    # Create a GroqModel instance
    model = construct_model(config=model_config)

    # Chat with the model
    user_query = "Can you get me a random city and the weather forecast for it?"
    raw_response = model.chat(user_query)
    #print(raw_response)

    # Create a ModelResponse object from the response
    model_response = ChainedFNCResponse.from_raw_response(raw_response=raw_response)
    print(model_response)

    # Create a FunctionCallingEngine instance
    fnc_engine = FunctionCallingEngine()
    fnc_engine.add_user_functions("static/sample_functions.py")

    # Call the functions from the model response
    outputs = fnc_engine.call_functions(model_response.function_calls)
    print(outputs)

def build_arg_parser():
    """ Build an argument parser for the script"""
    parser = argparse.ArgumentParser(description="Chained Function Calling Data Generation")
    parser.add_argument(
        "--flow",
        type=str,
        default="function_generating",
        help="The flow to execute",
    )
    return parser
    
def main():
    """Main function for the script"""
    # Parse the arguments
    arg_parser = build_arg_parser()
    args = arg_parser.parse_args()

    # Execute the flow based on the argument
    match args.flow:
        case "function_calling":
            function_calling_flow()
        case "function_generating" | "function_generation":
            schemas = generate_function_schemas(verbose=False, save=True)
        case _:
            print("Invalid flow. Please choose either 'function_calling' or 'function_generating'.")
    

if __name__ == "__main__":
    main()
from dotenv import load_dotenv

from src.models import construct_model      
from src.schemas import ChainedFNCResponse, FunctionsMetadata
from src.models.config import ModelConfig
from src.utils import load_fn_call_template, load_curriculum, save_function_schemas

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

def function_generating_flow():
    from src.components.function_schema_generator import FunctionSchemaGenerator

    # Create a ModelConfig instance
    model_config = ModelConfig(
        client="groq",
        system_prompt="You are a helpful assistant that generates function schemas.",
        temperature=0.7,
        fewshot_examples=None
    )
    generator = FunctionSchemaGenerator(model_config)

    # Load the curriculum
    curriculum = load_curriculum()
    
    # Generate schemas for each subcategory in the curriculum
    schemas = generator.generate_by_curriculum(curriculum, verbose=True)

    # Save the schemas to a JSON file
    save_function_schemas(schemas)
    

if __name__ == "__main__":
    #function_calling_flow()
    function_generating_flow()
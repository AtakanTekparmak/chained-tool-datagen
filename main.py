from dotenv import load_dotenv

from src.models.groq import GroqModel
from src.schemas import ChainedFNCResponse
from src.models.config import ModelConfig
from src.utils import load_fnc_template

from easy_fnc.function_caller import FunctionCallingEngine, create_functions_metadata
from easy_fnc.functions import get_user_defined_functions

def main():
    # Load the .env file
    load_dotenv()

    # Load the function call template
    fnc_template = load_fnc_template(
        fnc_metadata=create_functions_metadata(get_user_defined_functions("static/sample_functions.py"))
    )
    
    # Create a ModelConfig instance
    model_config = ModelConfig(
        name="llama3-70b-8192",
        system_prompt=fnc_template,
        temperature=0.5,
        fewshot_examples=None
    )
    # Create a GroqModel instance
    model = GroqModel(config=model_config)

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

if __name__ == "__main__":
    main()
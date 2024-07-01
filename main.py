from dotenv import load_dotenv

from src.models.groq import GroqModel
from src.schemas import ChainedFNCResponse
from src.models.config import ModelConfig
from src.utils import load_chained_fnc_prompt

from easy_fnc.function_caller import FunctionCallingEngine

def main():
    # Load the .env file
    load_dotenv()
    
    # Create a ModelConfig instance
    model_config = ModelConfig(
        name="llama3-70b-8192",
        system_prompt=load_chained_fnc_prompt(),
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
from dotenv import load_dotenv
import os

from src.models.groq import GroqModel
from src.schemas import ModelResponse

from easy_fnc.function_caller import FunctionCallingEngine

def main():
    # Load the .env file
    load_dotenv()
    
    # Create a GroqModel instance
    model = GroqModel()

    # Chat with the model
    user_query = "Can you get me a random city and the weather forecast for it?"
    raw_response = model.chat(user_query)
    #print(raw_response)

    # Create a ModelResponse object from the response
    model_response = ModelResponse.from_raw_response(raw_response=raw_response)
    print(model_response)

    # Create a FunctionCallingEngine instance
    fnc_engine = FunctionCallingEngine()
    fnc_engine.add_user_functions("static/sample_functions.py")

    # Call the functions from the model response
    outputs = fnc_engine.call_functions(model_response.function_calls)
    print(outputs)

if __name__ == "__main__":
    main()
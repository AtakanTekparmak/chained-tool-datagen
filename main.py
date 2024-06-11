from dotenv import load_dotenv
import os

from src.models.groq import GroqModel
from src.schemas import ModelResponse

def main():
    # Load the .env file
    load_dotenv()
    
    # Create a GroqModel instance
    model_name = os.environ.get("GROQ_BASE_MODEL")
    model = GroqModel(model_name=model_name)

    # Chat with the model
    user_query = "Can you send my friend (jasper3131@gmail.com) an email about the current sentiment about MMA in twitter and the stats for Sean Strickland please?"
    raw_response = model.chat(user_query)

    # Create a ModelResponse object from the response
    model_response = ModelResponse.from_raw_response(raw_response=raw_response)
    print(model_response)

if __name__ == "__main__":
    main()
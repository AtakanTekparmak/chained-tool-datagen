from dotenv import load_dotenv

from src.models.groq import GroqModel
from src.settings import MODEL_NAME

def main():
    # Load the .env file
    load_dotenv()
    
    # Create a GroqModel instance
    model = GroqModel(model_name=MODEL_NAME)

    # Chat with the model
    response = model.chat("Hello, how are you today?")

    # Print the response
    print(response)

if __name__ == "__main__":
    main()
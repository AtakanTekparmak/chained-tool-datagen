from src.models.groq import GroqModel
from src.models.config import ModelConfig
from src.models.model import Model

# Function to construct a model based on the client in the model config
def construct_model(config: ModelConfig) -> Model:
    if config.client == "groq":
        return GroqModel(config=config)
    else:
        raise ValueError(f"Client {config.client} not supported.")
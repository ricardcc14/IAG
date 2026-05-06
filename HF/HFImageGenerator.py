import requests
import io
from PIL import Image
import os
from huggingface_hub import InferenceClient

class HFImageGenerator:
    def __init__(self, token):
        self.token = token
        self.client = InferenceClient(api_key=self.token)

        self.available_models = {
            "FLUX": {
                "repo": "black-forest-labs/FLUX.1-schnell",
                "provider": "fal-ai"
            },
            "SDXL": {
                "repo": "stabilityai/stable-diffusion-xl-base-1.0",
                "provider": None  
            }
        }

    def requestImageGeneration(self, prompt, model_key="FLUX"):
        if model_key not in self.available_models:
            print(f"Model {model_key} not found in dictionary.")
            return None

        model_info = self.available_models[model_key]
        print(f"Requesting image from {model_key} ({model_info['repo']})...")

        try:
            image = self.client.text_to_image(
                prompt,
                model=model_info["repo"],
                provider=model_info["provider"]
            )
            return image
        
        except Exception as e:
            print(f"Error during {model_key} generation: {e}")
            return None
        


    

from huggingface_hub import InferenceClient
import os

class LlamaLLM:
    def __init__(self, token):
        self.model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
        self.token = token
        self.client = InferenceClient(model=self.model_id, token=self.token)

    def requestLLMResponse(self, user_prompt, system_instructions="Professional design senior"):
        try:
            response = self.client.chat_completion(
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=500,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}."

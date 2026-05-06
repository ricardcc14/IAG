from HFImageGenerator import HFImageGenerator
from LlamaLLM import LlamaLLM
from prompts import IMAGE_PROMPTS, TEXT_PROMPTS

class brandNewDAI():
    """
    brandNewDAI design agent
    """

    def __init__(self, token):
        self.token = token
        self.imgGen = HFImageGenerator(self.token)
        self.llm = LlamaLLM(self.token)

    """
        Combines brand details into a visual prompt and requests 
        the image generation.
    """

    def generateLogoFromScratch(self, brand_name, style, purpose, colors):
  
        prompt = IMAGE_PROMPTS["base_logo_design"].format(
            brand_name=brand_name, 
            style=style, 
            purpose=purpose,
            colors=colors
        )
        return self.imgGen.requestImageGeneration(prompt)


    """
        Requests the color palette strategy from the LLM.
        Returns the raw string (JSON-formatted text).
    """

    def generatePalette(self, brand_name, purpose):

        prompt = TEXT_PROMPTS["colour_palette"].format(
            brand_name=brand_name, 
            purpose=purpose
        )
        return self.llm.requestLLMResponse(prompt)

    """
        Requests the brand identity (mission, values, slogan) from the LLM.
        Returns the raw string (JSON-formatted text).
    """

    def generateIdentity(self, brand_name, purpose):

        prompt = TEXT_PROMPTS["brand_identity"].format(
            brand_name=brand_name, 
            purpose=purpose
        )
        return self.llm.requestLLMResponse(prompt)


    """
        Requests creative naming suggestions based on the purpose and style.
        Returns the raw string (JSON-formatted text).
    """

    def generateNaming(self, purpose, style):

        prompt = TEXT_PROMPTS["name_ideas"].format(
            purpose=purpose, 
            style=style
        )
        return self.llm.requestLLMResponse(prompt)
    

    """
    Requests the linguistic tone and voice definition for the brand.
    Returns the raw string (JSON-formatted text).
    """

    def generateTone(self, brand_name, purpose):

        prompt = TEXT_PROMPTS["brand_tone"].format(
            brand_name=brand_name, 
            purpose=purpose
        )
        return self.llm.requestLLMResponse(prompt)
  
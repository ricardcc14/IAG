import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Logic.stableDiffuser import SDXL_ControlNet

class logoGenerator(SDXL_ControlNet):
    def __init__(self):
        super().__init__()
        self.base_positive_prompt = "vector design, minimalist, flat design, geometric shapes, white background, high contrast, clean lines, professional branding, isoaltod on white"
        self.base_negative_prompt = "photorealistic, gradients, shadows, complex details, 3d render, shading, messy, blurry, low resolution"
        
    def generateLogoFromScratch(self, brand_name, style, purpose, colors):
        prompt = (
            f"Professional logo mark for {brand_name}, "
            f"representing {purpose}, {style} aesthetic, "
            f"color palette {colors}. "
            f"Logo must be {self.base_positive_prompt}"
        )
        
        print(f"Generating logo with prompt: {prompt}")
        self.generateImage("", "", False, prompt, self.base_negative_prompt)








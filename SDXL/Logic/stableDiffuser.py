import torch as torch
import cv2
import numpy as np
from transformers import DPTImageProcessor, DPTForDepthEstimation
from diffusers import DiffusionPipeline, ControlNetModel, StableDiffusionXLControlNetPipeline
from PIL import Image
import datetime

class SDXL_ControlNet:
    def __init__(self):
        self.device = "cuda"
        self.target_size = (640, 480) 

        self.depth_estimator = DPTForDepthEstimation.from_pretrained("Intel/dpt-hybrid-midas").to(self.device)
        self.feature_extractor = DPTImageProcessor.from_pretrained("Intel/dpt-hybrid-midas")
        self.controlnet = ControlNetModel.from_pretrained("diffusers/controlnet-canny-sdxl-1.0", torch_dtype=torch.float16, local_files_only=True)

        self.pipeline = StableDiffusionXLControlNetPipeline.from_pretrained("stabilityai/sdxl-turbo", controlnet=self.controlnet, torch_dtype=torch.float16, variant="fp16")
        self.pipeline.to(self.device)
        self.pipeline.vae.enable_slicing()

    # Utils functions for ControlNet generation
    # Edge detection (Canny method)
    def getCannyImage(self, image):
        img = np.array(image)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        edges = cv2.Canny(blur, 8, 10)
        edges = np.stack([edges]*3, axis=-1)
        return Image.fromarray(edges)

    # Depth estimation (DPT method)
    def getDepthMap(self, image):
        inputs = self.feature_extractor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.depth_estimator(**inputs)
            predicted_depth = outputs.predicted_depth
        
        prediction = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1),
            size=image.size[::-1],
            mode="bicubic",
            align_corners=False,
        )

        output = prediction.squeeze().cpu().numpy()
        formatted = (output * 255 / np.max(output)).astype("uint8")
        return Image.fromarray(formatted).convert("RGB")


    # Image generation logic
    def generateImage(self, inputPath, refPath, useREF, POS_prompt, NEG_prompt, CONTROLNET_MODE):

        USE_REF = useREF 
        CONTROLNET_NETS = {"CANNY" : "diffusers/controlnet-canny-sdxl-1.0", "DEPTH" : "diffusers/controlnet-depth-sdxl-1.0"}
        CONTROLNET_MODE = CONTROLNET_MODE
        PROMPT = POS_prompt
        NEGATIVE_PROMPT = NEG_prompt

        input_rgb = Image.open(inputPath).convert("RGB").resize(self.target_size)
        control_img = None

        if CONTROLNET_MODE == "CANNY":
            control_img = self.get_canny_image(input_rgb)
            control_img.save(f"Debug_Canny_ControlImage_{timestamp}.png")

        if CONTROLNET_MODE == "DEPTH":
            control_img = self.get_depth_map(input_rgb)
            control_img.save(f"Debug_Depth_ControlImage_{timestamp}.png")

        if CONTROLNET_MODE == "BOTH":
            control_1 = self.get_canny_image(input_rgb)
            control_1.save(f"Debug_Canny_ControlImage_{timestamp}.png")

            control_2 = self.get_depth_map(input_rgb)
            control_2.save(f"Debug_Depth_ControlImage_{timestamp}.png")

            control_img = [control_1, control_2]

        # Inference
        with torch.inference_mode():
            if USE_REF:
                ref_thermal = Image.open(refPath).convert("RGB").resize(self.target_size)
                output = self.pipeline(
                    prompt=PROMPT,
                    negative_prompt=NEGATIVE_PROMPT,
                    image=ref_thermal,
                    control_image=control_img, 
                    controlnet_conditioning_scale=1.0,
                    strength=1.0, 
                    guidance_scale=0.0, 
                    num_inference_steps=10
                ).images[0]
            else:
                output = self.pipeline(
                    prompt=PROMPT,
                    negative_prompt=NEGATIVE_PROMPT,
                    image=input_rgb, 
                    controlnet_conditioning_scale=1.0, 
                    guidance_scale=1.5, 
                    num_inference_steps=8,
                    height=self.target_size[1],
                    width=self.target_size[0]
                ).images[0]

        output.save(f"ControlNet_GeneratedImage_{timestamp}.png")
        print(f"Generation ended successfully!")











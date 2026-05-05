# SDXL Image Generation Module
Used as reference: https://huggingface.co/docs/diffusers/using-diffusers/controlnet.

SDXL is a latent diffusion model that can generate high-quality images from text prompts. 
As the model is very large, it is not possible to run it on a CPU. It requires a GPU with at least 8GB of VRAM.
The ControlNet logic has been added (Canny edge detection and Depth map) so that image variants can be created using restrictions by a control image.

## Libraries needed
To install all required Python libraries, please execute the following command on the Terminal: pip install -r requirements.txt.

The best way to execute it is to create a virtual environment first.
Having a virtual environment will allow you to have all the dependencies isolated from your system Python installation.

python -m venv .venv
.venv\Scripts\activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install opencv-python numpy diffusers transformers Pillow accelerate

## Logic folder
|___ Logic
|   |___ stableDiffuser.py
         This script is a Python parent class that uses the diffusers library to generate images using Stable Diffusion XL with ControlNet. It includes functions for edge detection (Canny), depth estimation (DPT), and image generation with ControlNet.
|   |___ logoGenerator.py
         This script is a Python class that inherits from SDXL_ControlNet and is used to generate logos. It includes functions for generating logos from scratch and modifying existing logos.
|___ 

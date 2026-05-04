## Method 1: Inference API (text tools)
from huggingface_hub import InferenceClient

client = InferenceClient()
def generate_palette(brand_name, style):
    prompt = f"""Generate a 5-color brand palette for a {style} brand called {brand_name}.
    Return ONLY a JSON array of hex codes. Example: ["#1a1a2e","#c8966e","#f5ecd7","#6b4c2a","#e8e0d0"]"""

    response = client.text_generation(
        prompt,
        model="mistralai/Mistral-7B-Instruct-v0.3",
        max_new_tokens=100
    )
    return response 

## Method 2: diffusers pipeline (image tools)
from diffusers import StableDiffusionXLPipeline
import torch, base64
from io import BytesIO

pipeline = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16
).to("cuda")
def generate_logo(brand_name, style, colors):
    prompt = f"minimalist logo mark for {brand_name}, {style} aesthetic, {colors} color palette, flat design, white background, vector style"

    image = pipe(prompt, num_inference_steps=30).images[0]

    # convert PIL image → base64 string to send to your JS frontend
    buf = BytesIO()
    image.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return b64
###################################
## Flask routes
###################################
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # lets your HTML file call this from the browser

@app.route("/api/palette", methods=["POST"])
def palette_route():
    body = request.json
    result = generate_palette(body["brand_name"], body["style"])
    return jsonify({"palette": result})

@app.route("/api/logo", methods=["POST"])
def logo_route():
    body = request.json
    b64 = generate_logo(body["brand_name"], body["style"], body["colors"])
    return jsonify({"image_base64": b64})

if __name__ == "__main__":
    app.run(port=5000)
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
import os
import uuid
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Use absolute paths to avoid issues with CWD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'user', 'uploads')
MEDIA_FOLDER = os.path.join(BASE_DIR, 'user', 'media')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg', 'ai'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MEDIA_FOLDER'] = MEDIA_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MEDIA_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/api/palette", methods=["POST"])
def palette_route():
    body = request.json
    result = generate_palette(body["brand_name"], body["style"])
    return jsonify({"palette": result})

@app.route("/api/logo", methods=["POST"])
def logo_route():
    try:
        body = request.json
        b64 = generate_logo(body["brand_name"], body["style"], body["colors"])
        
        filename = f"logo_{uuid.uuid4().hex}.png"
        filepath = os.path.join(app.config['MEDIA_FOLDER'], filename)
        
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(b64))
            
        return jsonify({
            "image_base64": b64,
            "saved_path": filepath
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/upload", methods=["POST"])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return jsonify({
                "message": "File uploaded successfully",
                "filename": filename,
                "path": filepath
            })
        else:
            return jsonify({"error": "File type not allowed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/files", methods=["GET"])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({"files": files})

@app.route("/api/files/<filename>", methods=["DELETE"])
def delete_file(filename):
    try:
        filename = secure_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({"message": "File deleted successfully"})
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=3000, debug=True)
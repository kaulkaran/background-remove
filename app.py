from flask import Flask, request, send_file, render_template, redirect, url_for 
from rembg import remove 
from PIL import Image 
import io 
import os


app = Flask(__name__) 
UPLOAD_FOLDER = 'static' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/') 
def index(): 
    return render_template('index.html', image_url=None)

@app.route('/remove-bg', methods=['POST']) 
def remove_bg(): 
    if 'image' not in request.files: 
        return "No image uploaded", 400

    file = request.files['image']
    input_bytes = file.read()
    output_bytes = remove(input_bytes)

# Convert to image and save
    img = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.png')
    img.save(output_path)

    return render_template('index.html', image_url=output_path)

@app.route('/download') 
def download(): 
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.png') 
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__': 
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port = port)

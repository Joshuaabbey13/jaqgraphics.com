from flask import Flask, request, send_file, render_template
from PIL import Image, ImageOps
import io

app = Flask(__name__)

def apply_sepia_filter(image):
    """Apply a sepia filter to an image."""
    if image.mode != 'RGB':
        image = image.convert('RGB')

    width, height = image.size
    pixels = image.load()

    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            if tr > 255:
                tr = 255
            if tg > 255:
                tg = 255
            if tb > 255:
                tb = 255

            pixels[px, py] = (tr, tg, tb)

    return image

def apply_grayscale_filter(image):
    """Apply a grayscale filter to an image."""
    return ImageOps.grayscale(image)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edit', methods=['POST'])
def edit_image():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        image = Image.open(file.stream)
        prompt = request.form.get('prompt', '').lower()

        # Mocking the "nana banana ai" by applying a filter
        if 'banana' in prompt:
            edited_image = apply_grayscale_filter(image)
        else:
            edited_image = apply_sepia_filter(image)

        byte_arr = io.BytesIO()
        edited_image.save(byte_arr, format='PNG')
        byte_arr.seek(0)

        return send_file(byte_arr, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

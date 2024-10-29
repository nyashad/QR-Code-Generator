from flask import Flask, render_template, request, send_file, abort
import qrcode
import io
import re
from PIL import Image

app = Flask(__name__)

# Simple regex for validating hex color codes
HEX_COLOR_REGEX = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')

def is_valid_color(color):
    return color in ["black", "white"] or HEX_COLOR_REGEX.match(color)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.get('data')
    fill_color = request.form.get('fill_color', 'black')
    back_color = request.form.get('back_color', 'white')
    file_type = request.form.get('file_type', 'png')  # Default to PNG if not specified
    
    if not data:
        return "No data provided", 400
    
    # Validate color input
    if not is_valid_color(fill_color) or not is_valid_color(back_color):
        return "Invalid color provided", 400

    try:
        # Create a QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)

        # Generate the image based on the selected format
        if file_type == 'svg':
            # SVG format
            img = qr.make_image(fill_color=fill_color, back_color=back_color, image_factory=qrcode.image.svg.SvgImage)
            img_bytes = io.BytesIO()
            img.save(img_bytes)
            img_bytes.seek(0)
            return send_file(img_bytes, mimetype='image/svg+xml', as_attachment=True, download_name='qrcode.svg')

        else:
            # Raster formats (PNG or JPEG)
            img = qr.make_image(fill_color=fill_color, back_color=back_color)
            img_bytes = io.BytesIO()

            if file_type == 'jpeg':
                img = img.convert("RGB")  # Convert to RGB for JPEG format
                img.save(img_bytes, format="JPEG")
                mimetype = 'image/jpeg'
                download_name = 'qrcode.jpeg'
            else:
                # Default to PNG
                img.save(img_bytes, format="PNG")
                mimetype = 'image/png'
                download_name = 'qrcode.png'

            img_bytes.seek(0)
            return send_file(img_bytes, mimetype=mimetype, as_attachment=True, download_name=download_name)

    except Exception as e:
        # Log the error message and return a 500 error
        print(f"Error generating QR code: {e}")
        abort(500, description="An error occurred while generating the QR code")

if __name__ == '__main__':
    app.run(debug=True)

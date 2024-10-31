from flask import Flask, render_template, request, send_file, abort
import qrcode
import io
import pandas as pd
import zipfile
import os
from PIL import Image
from qrcode.image.svg import SvgImage

app = Flask(__name__)

# Define the output folder
OUTPUT_FOLDER = 'output_qr_codes'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    fill_color = request.form.get('fill_color') or "black"
    selected_format = request.form.get('format')  # Get the selected format

    # Initialize a list to hold domain names
    domains = []

    # Handle URL input
    url = request.form.get('url')
    if url:
        domains.append(url)

    # Handle file upload
    if 'file' in request.files and request.files['file'].filename:
        file = request.files['file']
        
        # Read the file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
            domains.extend(df.iloc[:, 0].tolist())  # Assuming domain names are in the first column
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
            domains.extend(df.iloc[:, 0].tolist())  # Assuming domain names are in the first column
        else:
            return "Unsupported file format", 400

    if not domains:
        return "No URL or file provided", 400

    # Create output folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Create a zip file to store the QR codes
    zip_filename = os.path.join(OUTPUT_FOLDER, 'qr_codes.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for domain in domains:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(domain)
            qr.make(fit=True)

            # Generate the QR code image
            if selected_format == 'svg':
                img = qr.make_image(image_factory=SvgImage)
                img_bytes = io.BytesIO()
                img.save(img_bytes)
                img_bytes.seek(0)
            elif selected_format == 'png':
                # Create a transparent PNG by using RGBA mode
                img = qr.make_image(fill_color=fill_color, back_color="white")
                img = img.convert("RGBA")
                # Set background to transparent where applicable
                datas = img.getdata()
                new_data = []
                for item in datas:
                    if item[:3] == (255, 255, 255):  # White background pixels
                        new_data.append((255, 255, 255, 0))  # Convert to transparent
                    else:
                        new_data.append(item)
                img.putdata(new_data)

                img_bytes = io.BytesIO()
                img.save(img_bytes, format="PNG")
            else:
                # For JPEG and other formats
                img = qr.make_image(fill_color=fill_color, back_color="white")
                img_bytes = io.BytesIO()
                img.save(img_bytes, format=selected_format.upper())  # Save in the selected format

            img_bytes.seek(0)

            # Save the QR code to the zip file
            zipf.writestr(f"{domain}.{selected_format}", img_bytes.getvalue())

    return send_file(zip_filename, as_attachment=True, download_name='qr_codes.zip')

if __name__ == '__main__':
    app.run(debug=True)

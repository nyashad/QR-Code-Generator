from flask import Flask, render_template, request, send_file, abort
import qrcode
import io
import pandas as pd
import zipfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    fill_color = request.form.get('fill_color') or "black"
    back_color = request.form.get('back_color') or "transparent"

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

    # Create a zip file to store the QR codes
    zip_filename = 'qr_codes.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for domain in domains:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(domain)
            qr.make(fit=True)

            img = qr.make_image(fill_color=fill_color, back_color=back_color if back_color != "transparent" else None)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)

            # Save the QR code to the zip file
            zipf.writestr(f"{domain}.png", img_bytes.getvalue())

    return send_file(zip_filename, as_attachment=True, download_name=zip_filename)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, send_file, abort
import qrcode
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.get('data')
    fill_color = request.form.get('fill_color', 'black')
    back_color = request.form.get('back_color', 'white')
    
    if not data:
        return "No data provided", 400
    
    try:
        # Create a QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        # Save the image to a bytes buffer
        img_bytes = io.BytesIO()
        img.save(img_bytes)
        img_bytes.seek(0)

        return send_file(img_bytes, mimetype='image/png', as_attachment=True, download_name='qrcode.png')
    
    except Exception as e:
        # Return a 500 error for any unexpected issues
        print(f"Error generating QR code: {e}")
        abort(500, description="Error generating QR code")

if __name__ == '__main__':
    app.run(debug=True)

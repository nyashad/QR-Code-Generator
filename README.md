# QR Code Generator

[![Watch the video](https://img.youtube.com/vi/BYmzY_10QN0/0.jpg)](https://youtu.be/BYmzY_10QN0?autoplay=1&loop=1&playlist=BYmzY_10QN0)

## Overview
This project is a web application built with Flask that allows users to generate QR codes from a single URL or a list of domain names provided through a CSV or Excel file. Users can customize the QR codes' colors and select different image formats for download.

## Features
- Generate QR codes for a single URL or multiple URLs from an uploaded CSV or Excel file.
- Customisable QR code colors (fill and background).
- Choose from different image formats: PNG, JPEG, and SVG.
- Output is saved as a ZIP file containing all generated QR codes.

## Requirements
To run this project, you need:
- Python 3.x
- Flask
- pandas
- qrcode
- Pillow
- openpyxl (for Excel support)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/nyashad/QR-Code-Generator
   cd qr-code-generator

2. Create a virtual environment:

   - bash

   - python -m venv venv

3. Activate the virtual environment:

   - venv\Scripts\activate

    - Install the required packages:

    - pip install Flask pandas qrcode[pil] openpyxl

 4. Start the Flask application:

    - python app.py

## Open your web browser and navigate to http://127.0.0.1:5000.

### Fill in the form:
    - Enter a URL in the provided input field.
    - Optionally, upload a CSV or Excel file containing a list of domain names.
    - Select the desired image format (PNG, JPEG, SVG).
    - Choose fill and background colors (optional).

## Click on the "Generate QR Codes" button. The application will process your request and provide a ZIP file for download containing the generated QR codes.

    - Output Folder

    - Generated QR codes are stored in an output_qr_codes folder. The ZIP file with the QR codes will be saved in this folder.

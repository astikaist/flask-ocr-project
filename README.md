# flask-ocr-project

A simple Flask application to perform OCR (Optical Character Recognition) on newspaper images.

## Overview
This project provides a REST API to extract text from images.  
It uses **Tesseract OCR** under the hood, along with OpenCV for image preprocessing.  
You can deploy it locally or on a server (e.g., Heroku, AWS, etc.).

## Features
- **Image Preprocessing**: Cleans newspaper images for better OCR accuracy.
- **Endpoint**: `GET /api/reader?url=<IMAGE_URL>` returns JSON with extracted text.
- **Flask**: Simple to run and extend.

## Requirements
- Python 3.x
- Tesseract OCR installed on your system
- (Optional) A virtual environment to keep dependencies isolated

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/astikaist/flask-ocr-project.git
   cd flask-ocr-project

2. **Create & activate a virtual environment** (recommended):
    ```bash
    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate

    # Windows (Command Prompt)
    python -m venv venv
    venv\Scripts\activate

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt

## Usage

1. **Run the Flask app**:

    ```bash
    python ocr.py

After it starts, by default it will be available at http://127.0.0.1:5000/.

2. **Test the endpoint**:  
    Open your browser (or use `curl`/Postman) and go to:

    ```bash
    http://127.0.0.1:5000/api/reader?url=<IMAGE_URL>
    //example: http://127.0.0.1:5000/api/reader?url=https://example.com/newspaper.jpg

The response is JSON, which should include the extracted title and content, along with confidence scores.

## Project Structure
    flask-ocr-project/
    │   ocr.py             # Main Flask app and OCR logic
    │   requirements.txt   # Project dependencies
    │   .gitignore         # Files/folders to ignore in Git
    │
    ├── tessdata/          # Tesseract traineddata files
    ├── tessdata2/         # Additional Tesseract traineddata
    └── images/            # Sample images for testing


## Contributing

Pull requests and issue reports are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License
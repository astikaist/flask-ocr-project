# flask-ocr-project

A simple Flask application to perform OCR (Optical Character Recognition) on newspaper images.

## Overview
### Live Demo: [Flask OCR Project](https://flask-ocr-project-production.up.railway.app)
This project provides a REST API and a web interface to extract text from uploaded images.  
It uses **Tesseract OCR** under the hood, along with OpenCV for image preprocessing.  
You can deploy it locally or on a server (e.g., Railway, AWS, etc.).

## Features
- **Image Upload**: Users can upload images via a web form.
- **OCR Processing**: Extracts text from newspaper images.
- **Flask API Endpoint**: Accepts image uploads via `POST /upload` and returns extracted text.
- **Web Interface**: Simple upload page for easy access.
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
   ```

2. **Create & activate a virtual environment** (recommended):
    ```bash
    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate

    # Windows (Command Prompt)
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### **Run the Flask app**:
```bash
python ocr.py
```

After it starts, by default, it will be available at **http://127.0.0.1:5000/**.

### **Upload an Image for OCR**
1. Open a browser and go to:
   ```
   http://127.0.0.1:5000/
   ```
2. Choose an image file and click **Upload & Process OCR**.
3. The server processes the image and returns extracted text in JSON format.

### **API Usage (cURL or Postman)**
You can also use the API directly by sending a `POST` request with an image:

```bash
curl -X POST -F "file=@yourimage.png" http://127.0.0.1:5000/upload
```

Example JSON Response:
```json
{
    "content": "Extracted content from the newspaper image.",
    "content_confidence": 92.8
    "title": "Extracted Title",
    "title_confidence": 95.2,
}
```

## Project Structure
```
flask-ocr-project/
│   ocr.py             # Main Flask app and OCR logic
│   requirements.txt   # Project dependencies
│   .gitignore         # Files/folders to ignore in Git
│
├── tessdata/          # Tesseract traineddata files
├── tessdata2/         # Additional Tesseract traineddata
└── images/            # Sample images for testing
```

## Contributing
Pull requests and issue reports are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License
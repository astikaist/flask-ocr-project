import flask
from flask import request, jsonify, render_template
import cv2
from skimage.filters import threshold_local, threshold_sauvola, threshold_niblack, threshold_otsu
import numpy as np
import imutils
# from pythonRLSA.rlsa import rlsa
from rlsa import rlsa
import math
from tesserocr import PyTessBaseAPI
from PIL import Image
from skimage import io
import os
from pdf2image import convert_from_bytes
import requests
from werkzeug.utils import secure_filename

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Set upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def content_titles_separator(image):
    im = image.copy()
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except:
        gray = image

    (thresh, binary) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    (contours, _) = cv2.findContours(~binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)

    mask = np.ones(image.shape[:2], dtype="uint8") * 255
    (contours, _) = cv2.findContours(~binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    heights = [cv2.boundingRect(contour)[3] for contour in contours]
    avgheight = sum(heights) / len(heights)

    for c in contours:
        [x, y, w, h] = cv2.boundingRect(c)
        if h > 2 * avgheight:
            cv2.drawContours(mask, [c], -1, 0, -1)

    value = max(math.ceil(x / 100), math.ceil(y / 100)) + 20
    mask = rlsa(mask, True, False, value)

    (contours, _) = cv2.findContours(~mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask2 = np.ones(image.shape, dtype="uint8") * 255

    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)
        if w > 0.50 * im.shape[1]:
            title = im[y: y + h, x: x + w]
            mask2[y: y + h, x: x + w] = title
            im[y: y + h, x: x + w] = 255

    return mask2, im

def sauvola_thresholding(image):
    try:
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Konversi ke grayscale
    except:
        image_gray = image  # Jika sudah grayscale, gunakan langsung

    ts = threshold_sauvola(image_gray)  # Hitung threshold Sauvola untuk setiap piksel
    sauvola = (image_gray > ts).astype("uint8") * 255  # Terapkan binarisasi (hitam-putih)
    return sauvola

def image_from_nparray(nparray):
    img = Image.fromarray(nparray)
    return img

def ocr_reader(image):
    try:
        with PyTessBaseAPI(path="./tessdata", lang="ind") as api:  # Inisialisasi PyTessBaseAPI dengan model bahasa Indonesia (ind.traineddata)
            api.SetImage(image) # Memuat gambar ke dalam API Tesseract untuk diproses
            data = api.GetUTF8Text() # Mendapatkan teks yang dikenali dari gambar dalam format UTF-8
            wordConfidence = np.average(api.AllWordConfidences())  # Menghitung rata-rata confidence score untuk setiap kata yang dikenali
        return data, wordConfidence
    except Exception as e:
        print(f"Error during OCR: {e}")
        return "", 0

def content_post_processing(text):
    context = text[0]
    sentences = context.split("\n")
    paraghrap = ""
    before = ""

    for sentence in sentences:
        if sentence[-1:] == "-":
            sentence = sentence[0:-1]
        else:
            sentence += " "

        if sentence != " ":
            paraghrap += sentence
        elif before != " ":
            paraghrap += "\n"
        else:
            paraghrap = paraghrap

        before = sentence

    return paraghrap

def title_post_processing(text):
    title = text[0]
    title = title.replace("\n", " ")
    return title

def preprocess_image_for_ocr(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    return binary

def ocr_process(image):
    # Gaussian blur
    preprocessed_image = preprocess_image_for_ocr(image)
    titles_content = content_titles_separator(preprocessed_image)

    # titles_content = content_titles_separator(image)
    
    if np.percentile(titles_content, 90) - np.percentile(titles_content, 10) > 200:
        titles_data = titles_content[0]
        content_data = titles_content[1]
    else:
        #sauvala thresholding
        # titles_data = sauvola_thresholding(titles_content[0])
        # content_data = sauvola_thresholding(titles_content[1])
        
        titles_data = titles_content[0]  # No Sauvola used, just using the content
        content_data = titles_content[1]

    # Perform OCR for title and content
    title_text, title_confidence = ocr_reader(image_from_nparray(titles_data))
    content_text, content_confidence = ocr_reader(image_from_nparray(content_data))

    # Return as a dictionary
    return {
        "title": title_text,
        "title_confidence": title_confidence,
        "content": content_text,
        "content_confidence": content_confidence
    }

def ocr_process_pdf(url):
    pdf_file = requests.get(url)
    images = convert_from_bytes(pdf_file.content)
    hasil = {}
    print(len(images))
    x = 1

    for image in images:
        cvformat = np.array(image)[:, :, ::-1].copy()  # Convert to OpenCV format
        hasil[f"Page {x}"] = ocr_process_img(cvformat)
        x += 1

    return hasil

def ocr_process_img(image):
    result = ocr_process(image)
    return result

# upload image
@app.route("/")
def upload_page():
    return '''
    <!doctype html>
    <html lang="en">
    <head>
        <title>Upload Image for OCR</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f4f4f4;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            .upload-container {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                width: 40%;
                margin: auto;
            }
            input[type="file"] {
                margin: 10px 0;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            input[type="submit"] {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            input[type="submit"]:hover {
                background-color: #218838;
            }
        </style>
    </head>
    <body>
        <div class="upload-container">
            <h1>Welcome to OCR Reader for Newspaper</h1>
            <p>Upload an image and get the extracted text.</p>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <br>
                <input type="submit" value="Upload & Process OCR">
            </form>
        </div>
    </body>
    </html>
    '''

# Route to handle file upload and process OCR
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Read the image using OpenCV
    image = cv2.imread(filepath)
    results = ocr_process_img(image)

    return jsonify(results)

if __name__ == "__main__":
    # Check if running on a cloud server (Railway)
    is_production = os.getenv("RAILWAY_ENVIRONMENT") is not None
    
    if is_production:
        # Production mode (public access)
        app.run(host="0.0.0.0", port=5000, debug=False)
    else:
        # Local development mode
        app.run(debug=True)

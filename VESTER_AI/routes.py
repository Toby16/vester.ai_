from VESTER_AI import app
from flask import request, jsonify
import os
from PyPDF2 import PdfReader
import pprint


# Set the directory where uploaded files will be saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Allowed extensions
ALLOWED_EXTENSIONS = {'pdf', 'ppt', 'pptx'}
ALLOWED_MIME_TYPES = {'application/pdf', 'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'}

def allowed_file(filename, file):
    # Check file extension
    extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    if extension not in ALLOWED_EXTENSIONS:
        return False

    # Check MIME type
    if file.mimetype not in ALLOWED_MIME_TYPES:
        return False

    return True


@app.route('/')
def index():
    return {
        "statusCode": 200,
        "message": "nothing to see here!"
    }


@app.route('/upload', methods=['POST'])
def upload_file():
    #  [ VALIDATE REQUEST - Check if the post request has the file part ]
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']

    """
    If user does not select file, browser also
    submits an empty part without filename
    """
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename, file):
        # Save the file to the specified folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        try:
            # for pdf
            reader = PdfReader(file.filename)
            meta = reader.metadata

            number_of_pages = len(reader.pages)
            texts = {}

            for i in range(1, number_of_pages):
                page = reader.pages[i]
                text = page.extract_text()
                texts[i] = text
        except Exception as e:
            raise
            return str(e)

        pprint.pprint(texts)
        return jsonify({
            "statusCode": 200,
            "message": "File successfully uploaded",
            "working_dir": os.getcwd(),
            "file_path": file_path,
            "file_name": file.filename,
            "reader": {
                "number_of_pages": number_of_pages,
                "title": meta.title,
                # "texts": texts
            }
        })
    else:
        return jsonify({"error": "Invalid file type. Only PDF and PowerPoint files are allowed."}), 400


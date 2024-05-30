from VESTER_AI import app
from flask import request, jsonify
import os


# Set the directory where uploaded files will be saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return {
        "statusCode": 200,
        "message": "nothing to see here!"
    }


@app.route('/upload', methods=['POST'])
def upload_file():
    #  [ VALIDATE REQUEST - Check if the post request has the file part ]
    print(request.files)
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']

    """
    If user does not select file, browser also
    submits an empty part without filename
    """
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        # Save the file to the specified folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify(
        {
            "statusCode": 200,
            "message": "File successfully uploaded",
            "file_path": file_path,
            "file_name": file.filename
        })

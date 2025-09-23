from flask import Blueprint, request, jsonify
from app.model.huggingface import image_editing
from app.main.config import compress_image
import os
import json
import logging

main_bp = Blueprint('main', __name__)

# Configuration
IMAGE_FOLDER = './data/user_image'
JSON_FOLDER = './data/json'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

# Ensure upload directory exists
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(JSON_FOLDER, exist_ok=True)

# Global object to store data
class DataStore:
    def __init__(self):
        self.image_path = None
        self.text_data = None
        
    def update(self, image_path, text):
        self.image_path = image_path
        self.text_data = text

# Create global instance
data_store = DataStore()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main_bp.route('/health', methods=['GET'])
def health_check():
    logging.info("Health check endpoint accessed.")
    return jsonify({'status': 'healthy'}), 200

@main_bp.route('/upload', methods=['POST'])
def upload_data():
    # Check if inputs are present
    if 'image' not in request.files or 'text' not in request.form:
        return jsonify({'error': 'Missing inputs'}), 400
    
    file = request.files['image']
    text = request.form['text']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        
        filename = 'image' + '.jpg'
        filepath = os.path.join(IMAGE_FOLDER, filename)
        
        temp_path = filepath + '.temp'
        file.save(temp_path)
        
        # Check file size
        file_size = os.path.getsize(temp_path)
        max_size = 4 * 1024 * 1024
        
        compression_message = "Data uploaded successfully"
        
        if file_size > max_size:
            # Compress the image
            compressed_data = compress_image(temp_path)
            
            # Save the compressed image
            with open(filepath, 'wb') as f:
                f.write(compressed_data)
            
            compression_message = "Image has been compressed."
        else:
            # File is within size limit, just move it
            os.rename(temp_path, filepath)
            temp_path = None
        
        # Remove temporary file if it still exists
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        
        # Store data in global object
        data_store.update(filepath, text)
        
        # Also save to JSON file
        data_dict = {'image_path': filepath, 'text_data': text}

        jsonname = 'data' + '.json'
        jsonpath = os.path.join(JSON_FOLDER, jsonname)

        with open(jsonpath, 'w') as f:
            json.dump(data_dict, f)
        
        # Execute Hugging Face model after processing
        try:
            model_result = image_editing()
        except Exception as e:
            return jsonify({
                'error': f'Model execution failed: {str(e)}',
                'message': compression_message,
                'image_path': filepath,
                'text': text
            }), 500
        
        logging.info("Data upload and processing completed successfully.")

        return jsonify({
            'message': compression_message,
            'image_path': filepath,
            'text': text,
            'model_result': 'Image Generated Successfully'
        }), 200
    
    return jsonify({'error': 'Invalid file format. Only JPG files allowed'}), 400

# @main_bp.route('/get-data', methods=['GET'])
# def get_data_endpoint():
#     return jsonify({
#         'image_path': data_store.image_path,
#         'text_data': data_store.text_data
#     }), 200


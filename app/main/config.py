from PIL import Image
import io
import json
import os

# Function to compress image
def compress_image(image_path, max_size_mb=4):
    with Image.open(image_path) as img:
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        quality = 95
        while True:
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            size = buffer.tell()
            
            if size <= max_size_mb * 1024 * 1024:
                buffer.seek(0)
                return buffer.getvalue()
            
            quality -= 5
            if quality < 10:
                # If still too large, resize the image
                img = img.resize((int(img.width * 0.9), int(img.height * 0.9)), Image.Resampling.LANCZOS)
                quality = 95


def process_data():
    try:
        if os.path.exists('./data/json/data.json'):
            with open('./data/json/data.json', 'r') as f:
                data = json.load(f)
            image_path = data['image_path']
            text_data = data['text_data']

            return image_path, text_data
        
        else:
            print("No data file found. Please upload data first.")
        
    except Exception as e:
        print(f"Error reading data file: {e}")
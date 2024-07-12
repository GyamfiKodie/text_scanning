from flask import Flask, jsonify, request
import base64
import io
from PIL import Image
import ocr
import multiprocessing


app = Flask(__name__)

# Initialize a dictionary
data = {}


# Endpoint to add or update an item
@app.route('/item/<key>', methods=['POST'])
def add_or_update_item(key):
    value = request.json.get('value')
    data[key] = value
    return jsonify({'message': f'Item "{key}" updated successfully'}), 200

@app.route('/item/image', methods=['POST'])
def process_images():
    pytesseract = ocr.OCRLevelsExtraction()
    try:
        # Get image data from request
        images_data = request.json.get('images')
        print("images received")

        #extracted_texts = []

        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            extracted_texts = pool.map(pytesseract.pyTesseract,images_data)

        return jsonify({'message': 'Images received and processed successfully', 'extracted_texts': extracted_texts})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to process images', 'details': str(e)}), 500



# Endpoint to delete an item
@app.route('/item/<key>', methods=['DELETE'])
def delete_item(key):
    if key in data:
        del data[key]
        return jsonify({'message': f'Item "{key}" deleted successfully'}), 200
    else:
        return jsonify({'error': f'Item "{key}" not found'}), 404


# Endpoint to get all items
@app.route('/items', methods=['GET'])
def get_all_items():
    return jsonify(data), 200


# Endpoint to get a specific item
@app.route('/item/<key>', methods=['GET'])
def get_item(key):
    if key in data:
        return jsonify({key: data[key]}), 200
    else:
        return jsonify({'error': f'Item "{key}" not found'}), 404


if __name__ == '__main__':
    app.run(debug=True,host='64.23.199.187')


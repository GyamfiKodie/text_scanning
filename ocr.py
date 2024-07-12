from PIL import Image
import base64
import pytesseract
import io
from PIL import Image

class OCRLevelsExtraction:
    def __init__(self):
        # Path to Tesseract executable (change this according to your installation)
        pass

    def pyTesseract(self,image_data):
        try:
            # Open the image file
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
        
            # Use pytesseract to extract text
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print("Error:", e)
            return None

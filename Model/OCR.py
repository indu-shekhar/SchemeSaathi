import cv2
import pytesseract
from googletrans import Translator
import easyocr


def identify_document_type(text):
    """
    Identify document type based on extracted text.
    """
    print(len(document_keywords))
    
    try:
        print(text.lower())
        for doc_type, keywords in document_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    return doc_type
        return "Unknown Document"
    except Exception as e:
        return "Error in identifying document type."

def translate_to_english(text):
    """
    Translate text to English using Google Translate.
    """
    try:
        # Initialize the translator
        translator = Translator()
        # Translate text
        translation = translator.translate(text, dest='en')
        return translation.text
    except Exception as e:
        return text 

def easyocr_extract_text(image_path):
    reader = easyocr.Reader(['hi','en'])
    result = reader.readtext(image_path)
    text = ""
    for i in result:
      text += i[1] + " "

    text1 = translate_to_english(text)
    document_type = identify_document_type(text1.strip())
    return document_type


def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    return gray

def create_image_pyramid(image, scales=[0.5, 1, 1.5, 2]):
    """
    Generate an image pyramid with different scales.
    """
    pyramid_images = []
    for scale in scales:
        # Resize image according to the scale
        resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale)
        pyramid_images.append(resized_image)
    return pyramid_images

def extract_text_from_pyramid(image_pyramid):
    """
    Perform OCR on all images in the pyramid and return combined results.
    """
    extracted_text = ""
    for img in image_pyramid:
        # Apply thresholding for better OCR accuracy
        _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
        
        # Perform OCR
        text = pytesseract.image_to_string(thresh)
        extracted_text += text + "\n"
    return extracted_text


# Main Functionality
def main_for_ocr(img_path):
    image_path = img_path # Replace with your image path
    gray_image = preprocess_image(image_path)

    # Create the image pyramid
    image_pyramid = create_image_pyramid(gray_image)

    # Extract text from the pyramid
    extracted_text = extract_text_from_pyramid(image_pyramid)
    document_type = identify_document_type(extracted_text)
    if(document_type == "Unknown Document"):
        document_type = easyocr_extract_text(image_path)
    print(f"Document Type: {document_type}")
    return document_type
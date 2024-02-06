from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import io, os
from PIL import Image
import fitz  # PyMuPDF

# Set your Azure subscription key and endpoint
subscription_key = os.getenv('key')
endpoint = os.getenv('endpoint')
# Authenticate using your subscription key
credentials = CognitiveServicesCredentials(subscription_key)

# Create a ComputerVisionClient
client = ComputerVisionClient(endpoint, credentials)

def perform_ocr(image_data):
    # Perform OCR
    ocr_result = client.recognize_printed_text_in_stream(io.BytesIO(image_data))

    # Extract text from OCR result
    extracted_text = ""
    for region in ocr_result.regions:
        for line in region.lines:
            for word in line.words:
                extracted_text += word.text + " "
            extracted_text.strip()
            extracted_text += "\n"

    return extracted_text

def extract_images_from_pdf(pdf_file):
    # Open the PDF file
    pdf_document = fitz.open(pdf_file)

    extracted_text = []

    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        image_list = page.get_images(full=True)
        
        # Iterate through each image
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]

            # Perform OCR on the image data
            text = perform_ocr(image_bytes)
            extracted_text.append(text)

    # Close the PDF document
    pdf_document.close()

    return extracted_text

# Example usage
pdf_file = r"C:\Users\yough\Downloads\discussion.pdf"
extracted_text = extract_images_from_pdf(pdf_file)
for text in extracted_text:
    print(text)

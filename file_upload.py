import os
import requests
from dotenv import load_dotenv
import fitz  # PyMuPDF

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Set the path to your PDF file
pdf_path = "/Users/pbotin/Documents/SolarAPP_Foundation/GoogleDrive_Materials/01_Input_SLDs/For_Training_Examples/SA20250410-5395-123-336.pdf"
output_png_path = "/Users/pbotin/Documents/SolarAPP_Foundation/ELM/ELM_SLD2JSON/SA20250410-5395-123-336.png"

# Convert first page of PDF to PNG using PyMuPDF
doc = fitz.open(pdf_path)
page = doc.load_page(0)  # First page
pix = page.get_pixmap(dpi=200)
pix.save(output_png_path)

# Upload the converted PNG file
with open(output_png_path, "rb") as f:
    response = requests.post(
        "https://api.openai.com/v1/files",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file": (os.path.basename(output_png_path), f)},
        data={"purpose": "user_data"},
    )
    print(response.json())


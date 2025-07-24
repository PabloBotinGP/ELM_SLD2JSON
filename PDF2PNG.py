import fitz  # PyMuPDF

pdf_path = "SA20250312-242-105-1759.pdf"
output_path = pdf_path.replace(".pdf", ".png")

# Open the PDF
doc = fitz.open(pdf_path)

# Get the first page
page = doc.load_page(0)

# Render page to an image (pixmap)
pix = page.get_pixmap(dpi=300)  # Higher dpi = better resolution

# Save the image
pix.save(output_path)
print(f"✅ Saved: {output_path}")
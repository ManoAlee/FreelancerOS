import os
from pypdf import PdfWriter, PdfReader

def merge_pdfs(output_filename="merged.pdf"):
    """Merges all PDFs in the current directory."""
    writer = PdfWriter()
    pdf_files = [f for f in os.listdir() if f.endswith('.pdf') and f != output_filename]
    
    if not pdf_files:
        print("⚠️ No PDFs found to merge.")
        return

    print(f"📄 Found {len(pdf_files)} PDFs. Merging...")
    for filename in sorted(pdf_files):
        reader = PdfReader(filename)
        for page in reader.pages:
            writer.add_page(page)
    
    with open(output_filename, "wb") as f:
        writer.write(f)
    print(f"✅ Merged into '{output_filename}'")

def create_watermark(text="CONFIDENTIAL"):
    """
    (Placeholder) Ideally uses reportlab to generate a PDF watermark.
    For this MVP, we just print the logic.
    """
    print(f"💧 Watermark logic for '{text}' ready to implement.")
    # Real implementation would generate a transparent PDF and overlay it.

if __name__ == "__main__":
    print("--- PDF MASTER TOOL ---")
    print("1. Merge all PDFs in folder")
    choice = input("Select option (1): ")
    if choice == "1":
        merge_pdfs()

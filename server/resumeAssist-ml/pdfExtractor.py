import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text("text")  # "text" mode keeps layout & spacing
    return text.strip()

if __name__ == "__main__":
    file_name = "resume.pdf"  # Change this if your file name is different
    extracted_text = extract_text_from_pdf(file_name)

    # Optional: Save to .txt for inspection
    with open("extracted_resume.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)

    print("\n✅ Extracted Resume Text:\n")
    print(extracted_text[:3000])  # limit to 3k chars for readability

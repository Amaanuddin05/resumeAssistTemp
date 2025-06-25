import sys
import fitz
import re

def clean(text):
    # Remove non-ASCII junk
    text = re.sub(r'[^\x20-\x7E\n]', '', text)

    # Add newlines before section headings
    headings = [
        "Technical Skills", "Projects", "Experience",
        "Education", "Achievements", "Certifications"
    ]
    for h in headings:
        text = re.sub(rf'(?i)(?<!\n)({h})', r'\n\n\1', text)

    # Replace bullet symbols with dashes
    text = text.replace("•", "- ")

    # Add line breaks after periods for readability
    text = re.sub(r'\.\s+', '.\n', text)

    # Collapse multiple spaces
    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    print("🔥 CLEAN FUNCTION CALLED", file=sys.stderr)
    return clean(text)

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    print(extract_text_from_pdf(pdf_path))

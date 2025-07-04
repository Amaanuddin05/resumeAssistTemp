import pypdf
import docx
from io import BytesIO

class ResumeParser:
    def __init__(self):
        pass

    def extract_text_from_pdf(self, pdf_file):
        try:
            if hasattr(pdf_file, 'read'):
                file_content = pdf_file.read()
                pdf_file.seek(0)
            else:
                file_content = pdf_file

            pdf_reader = pypdf.PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                text += (page_text or "") + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def extract_text_from_docx(self, docx_file):
        try:
            doc = docx.Document(BytesIO(docx_file.read()))
            text = "\n".join(p.text for p in doc.paragraphs)
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""

    def extract_text(self, file):
        file.seek(0)
        if file.name.endswith('.pdf'):
            return self.extract_text_from_pdf(file)
        elif file.name.endswith('.docx'):
            return self.extract_text_from_docx(file)
        else:
            return ""

# ---------- TEST CODE ----------
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python test_parser.py <resume_file.pdf/docx>")
        exit(1)

    file_path = sys.argv[1]
    parser = ResumeParser()

    class NamedFile(BytesIO):
        def __init__(self, file_bytes, name):
            super().__init__(file_bytes)
            self.name = name

    try:
        with open(file_path, 'rb') as f:
            fake_file = NamedFile(f.read(), file_path)
            extracted_text = parser.extract_text(fake_file)

        txt_path = file_path.rsplit('.', 1)[0] + "_extracted.txt"
        with open(txt_path, "w", encoding="utf-8") as out_file:
            out_file.write(extracted_text)

        print(f"✅ Text extracted and saved to: {txt_path}")

    except Exception as e:
        print(f"❌ Failed to extract resume: {e}")

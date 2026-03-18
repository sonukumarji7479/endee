import pdfplumber
import io

class PDFProcessor:
    @staticmethod
    def extract_text(file_content: bytes) -> str:
        text = ""
        try:
             with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                  for page in pdf.pages:
                       extracted = page.extract_text()
                       if extracted:
                            text += extracted + "\n"
        except Exception:
             pass
        return text

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
         chunks = []
         i = 0
         while i < len(text):
              chunks.append(text[i:i+chunk_size])
              i += chunk_size - overlap
         return chunks

pdf_processor = PDFProcessor()

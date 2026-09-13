import io
from email import message_from_bytes
from email.policy import default
from pypdf import PdfReader
from docx import Document

class DocumentExtractionError(Exception):
    pass

def extract_text_from_document(filename: str, content: bytes) -> str:
    """Extracts raw text from uploaded document files based on extension."""
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    
    if ext == 'txt':
        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            raise DocumentExtractionError("Failed to decode TXT file. Must be valid UTF-8.")
            
    elif ext == 'pdf':
        try:
            reader = PdfReader(io.BytesIO(content))
            text = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
            full_text = "\n".join(text).strip()
            if not full_text:
                raise DocumentExtractionError("No text found in PDF. Scanned images are not supported.")
            return full_text
        except Exception as e:
            raise DocumentExtractionError(f"Failed to read PDF: {str(e)}")
            
    elif ext == 'eml':
        try:
            msg = message_from_bytes(content, policy=default)
            text = [
                f"Subject: {msg.get('subject', 'No Subject')}",
                f"From: {msg.get('from', 'Unknown')}",
                f"Date: {msg.get('date', 'Unknown')}",
                "\nBody:"
            ]
            
            body = msg.get_body(preferencelist=('plain', 'html'))
            if body:
                text.append(body.get_content())
            else:
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        text.append(part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8'))
                        break
                        
            return "\n".join(text).strip()
        except Exception as e:
            raise DocumentExtractionError(f"Failed to parse EML: {str(e)}")
            
    elif ext == 'docx':
        try:
            doc = Document(io.BytesIO(content))
            return "\n".join([paragraph.text for paragraph in doc.paragraphs]).strip()
        except Exception as e:
            raise DocumentExtractionError(f"Failed to parse DOCX: {str(e)}")
            
    else:
        raise DocumentExtractionError(f"Unsupported file type: {ext}")

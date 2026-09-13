import pytest
import io
from fastapi.testclient import TestClient
from app.main import app
from app.services.document_service import extract_text_from_document, DocumentExtractionError

client = TestClient(app)

# TEST 1: TXT extraction
def test_txt_extraction():
    content = b"Sample text content for complaint."
    text = extract_text_from_document("test.txt", content)
    assert text == "Sample text content for complaint."

# TEST 2: PDF text extraction (using a mock or relying on a real simple PDF generated if possible, but let's mock PdfReader to keep it fast, or use a tiny real PDF).
# We'll just test the error handling for now if content is invalid, and rely on the service logic.
def test_pdf_extraction_invalid():
    with pytest.raises(DocumentExtractionError):
        extract_text_from_document("test.pdf", b"not a real pdf")

# TEST 3: EML extraction
def test_eml_extraction():
    content = b"Subject: Test\nFrom: user@test.com\nDate: Today\n\nBody content."
    text = extract_text_from_document("test.eml", content)
    assert "Subject: Test" in text
    assert "Body content" in text

# TEST 4-6: Document extraction endpoint (mocking LangGraph)
from unittest.mock import patch
from app.schemas.ai import DocumentExtractionResult, RiskAssessment, ComplaintUpdates

def test_extract_document_endpoint():
    mock_result = DocumentExtractionResult(
        tool="extract_complaint_document",
        updates={"product_name": "Neurovit", "batch_number": "NV24081"},
        changed_fields=["product_name", "batch_number"],
        risk_assessment=RiskAssessment(severity="Major", priority="High"),
        recommended_actions=["QA Investigation"],
        explanation="Extracted fields from document."
    )

    with patch('app.api.ai.app_graph') as mock_graph:
        mock_graph.invoke.return_value = {
            "result": {
                "success": True,
                "tool": "extract_complaint_document",
                "result": mock_result.model_dump()
            }
        }
        
        file_content = b"Customer Complaint: Neurovit NV24081"
        response = client.post(
            "/api/ai/extract-document",
            files={"file": ("test.txt", file_content, "text/plain")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["filename"] == "test.txt"
        assert data["result"]["updates"]["product_name"] == "Neurovit"
        assert data["result"]["updates"]["batch_number"] == "NV24081"
        assert data["result"]["updates"].get("strength") is None # TEST 5: Missing fields remain null
        assert data["result"]["risk_assessment"]["severity"] == "Major" # TEST 6

# TEST 8: Unsupported file
def test_unsupported_file():
    response = client.post(
        "/api/ai/extract-document",
        files={"file": ("test.xyz", b"some content", "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]

# TEST 9: Oversized file
def test_oversized_file():
    # 10MB limit. Let's send 11MB.
    large_content = b"0" * (11 * 1024 * 1024)
    response = client.post(
        "/api/ai/extract-document",
        files={"file": ("large.txt", large_content, "text/plain")}
    )
    assert response.status_code == 413
    assert "File too large" in response.json()["detail"]

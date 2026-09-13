import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.schemas.ai import LogComplaintResult, EditComplaintResult, ComplaintUpdates, RiskAssessment

client = TestClient(app)

def test_log_then_edit_integration():
    """Test logging a complaint, then editing it immediately while it's still unsaved."""
    # 1. Log Complaint Mock
    mock_log_result = LogComplaintResult(
        tool="log_complaint",
        updates={"product_name": "Neurovit", "batch_number": "NV24081", "quantity_affected": "20 bottles"},
        changed_fields=["product_name", "batch_number", "quantity_affected"],
        risk_assessment=RiskAssessment(severity="Major", priority="High"),
        recommended_actions=["QA Investigation"],
        explanation="Initial log."
    )
    
    with patch('app.api.ai.app_graph') as mock_graph:
        mock_graph.invoke.return_value = {
            "result": {
                "success": True,
                "tool": "log_complaint",
                "result": mock_log_result.model_dump()
            }
        }
        
        # User says: A customer reported discolored capsules...
        log_response = client.post("/api/ai/chat", json={
            "message": "A customer reported discolored capsules for Neurovit 500 mg, batch NV24081. 20 bottles are affected.",
            "current_complaint": None
        })
        assert log_response.status_code == 200
        
        # In the real flow, the frontend updates Redux and passes this back for the next message.
        simulated_current_complaint = {
            "product_name": "Neurovit",
            "batch_number": "NV24081",
            "quantity_affected": "20 bottles"
        }
        
        # 2. Edit Complaint Mock
        mock_edit_result = EditComplaintResult(
            tool="edit_complaint",
            message="Batch number is NV24082 and quantity is 35 bottles.",
            updates={"batch_number": "NV24082", "quantity_affected": "35 bottles"},
            changed_fields=["batch_number", "quantity_affected"],
            risk_changed=False
        )
        
        mock_graph.invoke.return_value = {
            "result": {
                "success": True,
                "tool": "edit_complaint",
                "result": mock_edit_result.model_dump()
            }
        }
        
        # User says: Actually the batch is NV24082 and quantity is 35 bottles.
        edit_response = client.post("/api/ai/chat", json={
            "message": "Correction: the batch number is NV24082 and quantity is 35 bottles.",
            "current_complaint": simulated_current_complaint
        })
        
        assert edit_response.status_code == 200
        data = edit_response.json()
        assert data["tool"] == "edit_complaint"
        assert data["result"]["updates"]["batch_number"] == "NV24082"
        assert data["result"]["updates"]["quantity_affected"] == "35 bottles"
        assert "product_name" not in data["result"]["updates"] # Unrelated data must not be overwritten
        
def test_general_query_with_context():
    """Test general query uses the current complaint context."""
    with patch('app.api.ai.app_graph') as mock_graph:
        mock_graph.invoke.return_value = {
            "result": {
                "success": True,
                "tool": "chat",
                "result": {"reply": "The batch number is NV24081."}
            }
        }
        
        response = client.post("/api/ai/chat", json={
            "message": "What is the batch number?",
            "current_complaint": {"batch_number": "NV24081"}
        })
        assert response.status_code == 200
        assert response.json()["tool"] == "chat"
        assert "NV24081" in response.json()["result"]["reply"]

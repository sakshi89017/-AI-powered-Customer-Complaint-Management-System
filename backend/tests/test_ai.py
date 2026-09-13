from unittest.mock import patch
from app.schemas.ai import LogComplaintResult, ComplaintUpdates, RiskAssessment, EditComplaintResult

def test_log_complaint_tool_mock(client):
    """
    Test the LangGraph routing and log_complaint tool execution 
    using a mocked AI response to ensure schema structure and 
    API flow work correctly.
    """
    # Create a mock result matching the structured output of gemma2-9b-it
    mock_result = LogComplaintResult(
        tool="log_complaint",
        updates=ComplaintUpdates(
            complaint_source="Customer",
            product_name="Neurovit",
            strength="500 mg",
            batch_number="NV24081",
            quantity_affected="20 bottles",
            complaint_type="Product Quality",
            description="Customer reported discolored capsules."
        ),
        risk_assessment=RiskAssessment(severity="Major", priority="High"),
        recommended_actions=["QA Investigation", "Batch Review"],
        changed_fields=["complaint_source", "product_name", "strength", "batch_number", "quantity_affected", "complaint_type", "description"],
        explanation="The complaint indicates a potential pharmaceutical product quality defect involving capsule discoloration."
    )

    with patch('app.agents.graph.invoke_log_complaint_tool') as mock_tool, \
         patch('app.agents.graph.ChatGroq') as MockChat:
        
        # Mock the intent detection to always return 'log_complaint' for this test
        mock_llm_instance = MockChat.return_value
        mock_llm_instance.with_structured_output.return_value.invoke.return_value.intent = "log_complaint"
        
        mock_tool.return_value = mock_result
        
        payload = {
            "message": "A customer reported discolored capsules for Neurovit 500 mg, batch NV24081. Around 20 bottles are affected."
        }
        
        response = client.post("/api/ai/chat", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["tool"] == "log_complaint"
        assert data["result"]["updates"]["product_name"] == "Neurovit"
        assert data["result"]["updates"]["batch_number"] == "NV24081"
        assert data["result"]["risk_assessment"]["severity"] == "Major"
        
def test_general_chat_mock(client):
    with patch('app.agents.graph.ChatGroq') as MockChat:
        mock_llm_instance = MockChat.return_value
        
        # Intent returns general_chat
        mock_llm_instance.with_structured_output.return_value.invoke.return_value.intent = "general_chat"
        # Chat response
        mock_llm_instance.invoke.return_value.content = "I am an AI assistant."
        
        payload = {"message": "Hello!"}
        response = client.post("/api/ai/chat", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["tool"] == "chat"
        assert data["result"]["reply"] == "I am an AI assistant."

def test_edit_complaint_tool_mock(client):
    mock_result = EditComplaintResult(
        tool="edit_complaint",
        updates={"batch_number": "NV24082", "quantity_affected": "35 bottles"},
        changed_fields=["batch_number", "quantity_affected"],
        risk_changed=False,
        message="Batch number and quantity updated successfully."
    )

    with patch('app.agents.graph.invoke_edit_complaint_tool') as mock_tool, \
         patch('app.agents.graph.ChatGroq') as MockChat:
        
        mock_llm_instance = MockChat.return_value
        mock_llm_instance.with_structured_output.return_value.invoke.return_value.intent = "edit_complaint"
        mock_tool.return_value = mock_result
        
        payload = {
            "message": "Change the batch number to NV24082 and quantity to 35 bottles.",
            "current_complaint": {
                "batch_number": "NV24081",
                "quantity_affected": "20 bottles",
                "product_name": "Neurovit"
            }
        }
        
        response = client.post("/api/ai/chat", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["tool"] == "edit_complaint"
        assert "batch_number" in data["result"]["updates"]
        assert "product_name" not in data["result"]["updates"]
        assert data["result"]["updates"]["batch_number"] == "NV24082"

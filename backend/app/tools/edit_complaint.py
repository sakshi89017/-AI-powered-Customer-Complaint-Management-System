import json
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

from app.schemas.ai import EditComplaintResult
from app.core.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """You are an expert AI Complaint Management Co-Pilot for a pharmaceutical company.
Your task is to execute the 'edit_complaint' tool.
You will be provided with the CURRENT COMPLAINT STATE and the USER'S REQUEST.

Rules:
1. ONLY modify fields that the user explicitly requested or that are clearly implied by their request.
2. DO NOT change, regenerate, or overwrite any fields the user did not ask to change.
3. If the user's request is ambiguous (e.g. "Update the quantity" but doesn't say to what), DO NOT modify any fields. Instead, set `updates` to empty, `changed_fields` to empty, and set `message` to a clarifying question (e.g., "What quantity should I set?").
4. Validate values:
   - Priority: Low, Medium, High, Urgent
   - Severity: Minor, Major, Critical
   - Status: Pending Triage, Under Investigation, QA Review, Action Required, Closed
5. Reassess Risk:
   - If the edit changes the nature of the issue (e.g. changing complaint type, description, or severity/priority directly), recalculate risk.
   - If recalculating risk, set `risk_changed` to true, and provide the new `risk_assessment` and `recommended_actions`.
   - If the edit does NOT affect risk (e.g. changing customer name, fixing a typo in batch number), set `risk_changed` to false, and leave risk fields null.

Return ONLY the fields that are changing in the `updates` dictionary.
"""

def invoke_edit_complaint_tool(message: str, current_complaint: dict) -> EditComplaintResult:
    """Invokes the Groq model to perform a partial update on a complaint."""
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL,
        temperature=0.0
    )
    
    structured_llm = llm.with_structured_output(EditComplaintResult)
    
    context = (
        f"CURRENT COMPLAINT STATE:\n{json.dumps(current_complaint, indent=2)}\n\n"
        f"USER REQUEST:\n{message}"
    )
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=context)
    ]
    
    result: EditComplaintResult = structured_llm.invoke(messages)
    
    # Clean up updates dictionary to ensure only changed fields are present and valid
    if result.updates:
        # Filter out keys that match the current state perfectly just in case the LLM returned them
        filtered_updates = {}
        for k, v in result.updates.items():
            if k in current_complaint and current_complaint[k] != v:
                filtered_updates[k] = v
            elif k not in current_complaint:
                filtered_updates[k] = v
                
        result.updates = filtered_updates
        result.changed_fields = list(filtered_updates.keys())
    
    return result

import json
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

from app.schemas.ai import LogComplaintResult
from app.core.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """You are an expert AI Complaint Management Co-Pilot for a pharmaceutical company.
Your task is to extract relevant information from the user's natural language complaint, categorize it, and perform an initial risk assessment.

Rules for Extraction:
1. Extract ONLY information that is explicitly stated or can be directly inferred from the text.
2. DO NOT invent missing values for product name, batch number, dates, quantity, etc. Leave them as null if not provided.
3. Classify the source appropriately (e.g., 'Customer', 'Email', 'Phone'). If not provided, use null.
4. Classify the complaint type (e.g., 'Product Quality', 'Packaging', 'Labeling', 'Distribution', 'Adverse Event', 'Suspected Counterfeit').
5. Preserve quantity units (e.g., '20 bottles').
6. Provide a concise summary for the 'description'.

Rules for Risk Assessment & Additional Checks:
1. Provide an initial 'severity' (Minor, Major, Critical).
2. Provide an initial 'priority' (Low, Medium, High, Urgent).
3. Base this on standard pharma QA principles.
4. Provide a list of 1-3 'recommended_actions' (e.g., 'QA Investigation', 'Batch Review').
5. Provide a plausible 'root_cause_recommendation' (e.g. 'Seal failure during primary packaging').
6. Provide a 'capa_recommendation' (e.g. 'Recalibrate sealing machine temperature').
7. Identify any 'missing_critical_fields'. Critical fields are: Product Name, Batch Number, and Quantity Affected. If any are missing, list their names.
8. Provide a short 'explanation' for your assessment.

You MUST respond strictly in the requested JSON structure that matches the LogComplaintResult schema.
"""

def invoke_log_complaint_tool(message: str, current_comp: dict = None) -> LogComplaintResult:
    """Invokes the Groq model to extract complaint details and returns the structured result."""
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL,  # e.g., "gemma2-9b-it"
        temperature=0.0
    )
    
    # We use with_structured_output to ensure the response matches the Pydantic model
    structured_llm = llm.with_structured_output(LogComplaintResult)
    
    context = message
    if current_comp:
        context = f"Current Complaint Context:\n{json.dumps(current_comp, indent=2)}\n\nNew input:\n{message}"
        
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=context)
    ]
    
    result: LogComplaintResult = structured_llm.invoke(messages)
    
    # Populate changed_fields based on non-null values in updates
    changed = []
    updates_dict = result.updates.model_dump(exclude_unset=True)
    for k, v in updates_dict.items():
        if v is not None:
            changed.append(k)
    result.changed_fields = changed
    
    return result

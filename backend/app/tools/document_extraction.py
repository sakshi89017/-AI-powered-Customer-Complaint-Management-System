from typing import List, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

from app.schemas.ai import DocumentExtractionResult
from app.core.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """You are an expert AI Document Extractor for a pharmaceutical Complaint Management System.
Your task is to analyze the raw text extracted from a customer document (PDF, Email, etc.) and map it to our structured complaint schema.

Rules:
1. Extract data precisely. DO NOT invent, guess, or hallucinate missing information.
2. If a field (e.g., batch number, strength) is not explicitly mentioned or clearly inferable, leave it as null/None.
3. Perform an initial risk assessment based on the severity of the issue described.
4. Recommend 1-3 appropriate QA actions (e.g., "QA Investigation", "Batch Hold", "Customer Follow-up").
5. Return ONLY the JSON object matching the requested schema.
6. The list `changed_fields` MUST include exactly the keys in `updates` that you provided a non-null value for.
7. Provide a plausible `root_cause_recommendation` and `capa_recommendation`.
8. Identify any `missing_critical_fields`. Critical fields are: Product Name, Batch Number, and Quantity Affected. If any are missing, list their names.

Note on schema mapping:
- 'Customer Name' -> customer_name
- 'Product' -> product_name
- 'Complaint' -> description
- 'Complaint Type' -> e.g. "Product Quality", "Adverse Event", "Packaging Defect"
"""

import json

def invoke_extract_document_tool(document_text: str, current_comp: dict = None) -> DocumentExtractionResult:
    """Invokes the Groq model to extract structured data from document text."""
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL,
        temperature=0.0
    )
    
    structured_llm = llm.with_structured_output(DocumentExtractionResult)
    
    context_str = ""
    if current_comp:
        context_str = f"Current Complaint Context:\n{json.dumps(current_comp, indent=2)}\n\n"
        
    context = (
        f"{context_str}EXTRACTED DOCUMENT TEXT:\n{document_text}\n\n"
        f"Please extract all relevant fields, assess risk, and return the structured object."
    )
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=context)
    ]
    
    result: DocumentExtractionResult = structured_llm.invoke(messages)
    
    # Filter changed fields to ensure accuracy
    if result.updates:
        extracted_dict = result.updates.model_dump(exclude_unset=True)
        result.changed_fields = [k for k, v in extracted_dict.items() if v is not None]
    
    return result

from typing import TypedDict, Optional, Dict, Any
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.schemas.ai import LogComplaintResult, EditComplaintResult
from app.tools.log_complaint import invoke_log_complaint_tool
from app.tools.edit_complaint import invoke_edit_complaint_tool

from app.tools.document_extraction import invoke_extract_document_tool

settings = get_settings()

class AgentState(TypedDict):
    messages: list[str]
    intent: Optional[str]
    result: Optional[dict]
    current_complaint: Optional[Dict[str, Any]]
    complaint_id: Optional[str]

class IntentClassification(BaseModel):
    intent: str = Field(description="Must be 'log_complaint' for a new complaint, 'edit_complaint' to modify an existing complaint, or 'general_chat' otherwise.")

def intent_detector(state: AgentState):
    """Detects if the user wants to log, edit, or chat."""
    # Note: 'extract_document' intent is bypassed by the API directly injecting the intent,
    # but we still want to not override it if it exists.
    if state.get("intent") == "extract_document":
        return {"intent": "extract_document"}
        
    last_message = state["messages"][-1]
    
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL,
        temperature=0.0
    )
    
    structured_llm = llm.with_structured_output(IntentClassification)
    prompt = (
        f"Determine the intent of the following message.\n"
        f"If reporting a NEW problem/complaint, classify as 'log_complaint'.\n"
        f"If the user wants to change, update, or correct an EXISTING complaint, classify as 'edit_complaint'.\n"
        f"Otherwise 'general_chat'.\n\nMessage: {last_message}"
    )
    
    classification = structured_llm.invoke([HumanMessage(content=prompt)])
    
    intent = classification.intent
    if intent == "edit_complaint" and not state.get("current_complaint"):
        intent = "log_complaint"
        
    return {"intent": intent}

def route_intent(state: AgentState):
    intent = state.get("intent")
    if intent == "log_complaint":
        return "log_complaint_node"
    elif intent == "edit_complaint":
        return "edit_complaint_node"
    elif intent == "extract_document":
        return "extract_document_node"
    return "general_chat_node"

def log_complaint_node(state: AgentState):
    """Executes the log_complaint tool."""
    last_message = state["messages"][-1]
    current_comp = state.get("current_complaint", {})
    try:
        tool_result = invoke_log_complaint_tool(last_message, current_comp)
        return {"result": {"success": True, "tool": "log_complaint", "result": tool_result.model_dump()}}
    except Exception as e:
        return {"result": {"success": False, "error": str(e)}}

def edit_complaint_node(state: AgentState):
    """Executes the edit_complaint tool."""
    last_message = state["messages"][-1]
    current_comp = state.get("current_complaint", {})
    try:
        tool_result = invoke_edit_complaint_tool(last_message, current_comp)
        return {"result": {"success": True, "tool": "edit_complaint", "result": tool_result.model_dump()}}
    except Exception as e:
        return {"result": {"success": False, "error": str(e)}}

def extract_document_node(state: AgentState):
    """Executes the extract_document tool on raw extracted text."""
    last_message = state["messages"][-1]
    current_comp = state.get("current_complaint", {})
    try:
        tool_result = invoke_extract_document_tool(last_message, current_comp)
        return {"result": {"success": True, "tool": "extract_complaint_document", "result": tool_result.model_dump()}}
    except Exception as e:
        return {"result": {"success": False, "error": str(e)}}

def general_chat_node(state: AgentState):
    """Handles general chit-chat."""
    last_message = state["messages"][-1]
    current_comp = state.get("current_complaint", {})
    
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL,
        temperature=0.7
    )
    
    system_prompt = "You are a helpful AI assistant for a pharmaceutical QA system. Be concise."
    if current_comp:
        system_prompt += f"\n\nCurrent Complaint Context:\n{current_comp}"
        
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=last_message)
    ])
    return {"result": {"success": True, "tool": "chat", "result": {"reply": response.content}}}

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("intent_detector", intent_detector)
workflow.add_node("log_complaint_node", log_complaint_node)
workflow.add_node("edit_complaint_node", edit_complaint_node)
workflow.add_node("extract_document_node", extract_document_node)
workflow.add_node("general_chat_node", general_chat_node)

workflow.add_edge(START, "intent_detector")
workflow.add_conditional_edges(
    "intent_detector",
    route_intent,
    {
        "log_complaint_node": "log_complaint_node",
        "edit_complaint_node": "edit_complaint_node",
        "extract_document_node": "extract_document_node",
        "general_chat_node": "general_chat_node"
    }
)
workflow.add_edge("log_complaint_node", END)
workflow.add_edge("edit_complaint_node", END)
workflow.add_edge("extract_document_node", END)
workflow.add_edge("general_chat_node", END)

app_graph = workflow.compile()

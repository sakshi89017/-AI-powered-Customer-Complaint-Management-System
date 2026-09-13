# Final Project Architecture

```ascii
                React UI
                   |
                 Redux
                   |
                   v
                FastAPI
                   |
                   v
               LangGraph
                   |
         +---------+---------+
         |         |         |
         v         v         v
       Log       Edit    Document
       Tool      Tool    Extraction
         |         |         |
         +---------+---------+
                   |
                   v
             Risk Assessment
                   |
                   v
              PostgreSQL
```

## Architectural Layers Explained

- **React UI:** The frontend presentation layer, providing an intuitive dashboard, complaint forms, and the conversational AI Co-Pilot interface.
- **Redux:** Acts as the single source of truth for the active complaint, seamlessly merging user edits and AI-extracted data.
- **FastAPI:** The high-performance Python backend that handles RESTful routing and strict Pydantic data validation.
- **LangGraph:** Orchestrates the AI workflow by detecting user intent and routing the execution to the appropriate tool.
- **Log / Edit / Document Extraction Tools:** Specialized Python scripts that leverage the LLM (Groq) to intelligently parse, structure, and patch specific fields of a complaint.
- **Risk Assessment:** A preliminary AI-generated evaluation of severity, priority, and recommended actions, generated alongside tool execution.
- **PostgreSQL:** The persistent relational database storing the final complaint records and maintaining an immutable audit trail of all changes.

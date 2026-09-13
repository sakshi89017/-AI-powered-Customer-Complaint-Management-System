# Evaluator Demo Workflow

This document provides a single, complete 5-minute workflow designed to demonstrate all major assignment requirements.

---

### STEP 1:
Navigate to the Dashboard and click **Log New Complaint**.

### STEP 2:
In the AI Co-Pilot chat, enter:
> *"A customer reported discolored capsules for Neurovit 500 mg, batch NV24081. 20 bottles are affected."*

### STEP 3:
Point out the **LOG_COMPLAINT** action occurring in the AI chat.

### STEP 4:
Show that the form on the left was automatically populated with the Product, Strength, Batch, and Quantity. Notice the pulsing "AI Updated" badges.

### STEP 5:
Show the **AI Initial Risk Assessment** card that appears in the chat, detailing Severity, Priority, and Recommended Actions.

### STEP 6:
In the AI Co-Pilot chat, enter:
> *"Correction: the batch number is NV24082 and quantity is 35 bottles."*

### STEP 7:
Point out the **EDIT_COMPLAINT** action occurring in the AI chat.

### STEP 8:
Show that **only the requested fields (Batch and Quantity) changed** on the form. The Product and Strength remain perfectly intact.

### STEP 9:
Click **Upload supporting document** in the Co-Pilot panel and upload:
`demo_data/sample_batch_quality_complaint.pdf`

### STEP 10:
Point out the **DOCUMENT_EXTRACTION** action as the UI reads the file.

### STEP 11:
Show the document-extracted information merging into the form (e.g., Customer details populate without erasing the existing product information).

### STEP 12:
In the AI Co-Pilot chat, enter:
> *"The affected quantity should be 42 bottles."*

### STEP 13:
Show that Edit Complaint works perfectly *after* document extraction, surgically updating the quantity to 42.

### STEP 14:
Click the blue **Save Complaint** button at the bottom of the form.

### STEP 15:
Navigate to the Complaints List and open the saved complaint.

### STEP 16:
Scroll to the bottom of the page to show the **Audit Trail**. It immutably records exactly what changed, what the old values were, and what the new values are.

---

## IMPORTANT THINGS TO NOTICE
- AI controls form population through natural language.
- AI can selectively edit existing data without erasing unrelated fields.
- AI can extract information from a document.
- The three tools (Log, Edit, Extract) operate seamlessly on the same active complaint.
- Redux keeps the active complaint state synchronized across the UI.
- LangGraph routes the AI workflow intelligently based on intent.
- Groq provides the underlying fast LLM inference.
- PostgreSQL stores the final complaint and the immutable audit events.
- Audit history records changes (old value vs. new value) for traceability.
- AI risk assessment is preliminary and explicitly requires QA review (indicated by the warning UI).

# Final Demonstration Script (5-10 Minutes)

Use this script to record your final 5-10 minute demonstration video for the evaluator.

---

## PART 1 — INTRODUCTION (0:00 - 0:45)
**Speak to the camera/mic:**
> "This is an AI-powered Customer Complaint Management System for the pharmaceutical manufacturing industry.
> 
> The goal is to help QA users capture, update, and process customer complaints using an AI Co-Pilot instead of manually entering every field.
> 
> The system uses React and Redux on the frontend, FastAPI on the backend, LangGraph for AI orchestration, Groq with `gemma2-9b-it` as the LLM, and PostgreSQL for persistence."

---

## PART 2 — SHOW THE UI (0:45 - 1:15)
1. **Show the Dashboard:** Point out the statistics.
2. **Show the Complaint List:** Point out the table layout.
3. **Open New Complaint:** Click "Log New Complaint".
4. **Point out the layout:** 
   - Left: The structured Complaint Form.
   - Right: The AI Co-Pilot chat interface.
   - Point out where the Risk Assessment, Recommended Actions, and Status will appear.

---

## PART 3 — LOG COMPLAINT DEMO (1:15 - 2:00)
1. In the AI Co-Pilot chat, enter exactly:
   > *"A customer reported discolored capsules for Neurovit 500 mg, batch NV24081. 20 bottles are affected."*
2. **Show the AI response:** Point out that it recognized the intent as `LOG_COMPLAINT`.
3. **Show the form:** Point out how the Product, Strength, Batch, Quantity, and Complaint Type fields automatically populated.
4. **Show the Risk Assessment:** Point out the generated Severity, Priority, and Recommended Actions (e.g., "QA Investigation").
5. **Explain explicitly:**
   > "The important part is that the user did not manually fill the form. The AI interpreted the natural-language complaint and populated the structured fields."

---

## PART 4 — SHOW CODE FOR LOG COMPLAINT (2:00 - 4:00)
Follow the `CODE_WALKTHROUGH.md` document for this section.
1. **Explain briefly during the code tour:**
   > "User input flows from React to FastAPI. FastAPI hands it to LangGraph, which routes to the `log_complaint` tool using Groq. The structured result is sent back, dispatched to Redux, and renders on the complaint form."

---

## PART 5 — EDIT COMPLAINT DEMO (4:00 - 5:00)
1. Using the same complaint from Part 3, enter exactly:
   > *"Correction: the batch number is NV24082 and the affected quantity is 35 bottles."*
2. **Show the AI response:** Point out that it selected `EDIT_COMPLAINT`.
3. **Show the form:** Point out that ONLY the Batch and Quantity changed. Product, Strength, and Description remained perfectly unchanged.
4. **Explain explicitly:**
   > "The Edit Complaint tool performs a differential/patch update. It changes only what the user requested instead of regenerating the entire complaint."

---

## PART 6 — DOCUMENT EXTRACTION DEMO (5:00 - 6:30)
1. **Click "Upload supporting document"** in the Co-Pilot panel.
2. Select and upload `sample_batch_quality_complaint.pdf` from the `demo_data/` folder.
3. **Show the AI response:** Point out that it selected `DOCUMENT_EXTRACTION`.
4. **Show the form:** Point out the extracted data merging into the form fields.
5. **Show the Risk Assessment:** Point out that the risk was assessed based on the document's text.
6. **Explain explicitly:**
   > "The document itself is processed first to extract text. That text is then passed into the LangGraph AI workflow for structured complaint extraction."

---

## PART 7 — EDIT AFTER DOCUMENT EXTRACTION (6:30 - 7:30)
1. In the AI chat, enter exactly:
   > *"The affected quantity should be 42 bottles."*
2. **Show the AI response:** Point out `EDIT_COMPLAINT` executing.
3. **Show the form:** Point out that only the quantity updated to 42.
4. **Explain explicitly:**
   > "This demonstrates that document extraction and natural-language editing operate on the same active complaint state."

---

## PART 8 — DATABASE AND AUDIT (7:30 - 8:30)
1. Click the blue **Save Complaint** button at the bottom of the form.
2. Navigate to the **Complaint List**.
3. Open the newly saved complaint.
4. **Scroll down to the bottom** of the page to show the **Audit Trail**.
5. **Show the history:** Point out how the batch changed (`NV24081 → NV24082`) and the quantity changed (`20 → 35 → 42`).
6. **Explain explicitly:**
   > "The audit trail preserves the sequence of changes rather than silently overwriting history."

---

## PART 9 — ARCHITECTURE (8:30 - 9:00)
1. Open `ARCHITECTURE.md` or `FINAL_ARCHITECTURE.md` on screen.
2. Briefly explain the layers:
   - **React:** Provides the UI and Co-Pilot.
   - **Redux:** Manages the active state and form updates.
   - **FastAPI:** Handles backend routing and validation.
   - **LangGraph:** Orchestrates the AI intent and tool routing.
   - **Groq:** Provides ultra-fast LLM inference.
   - **AI Tools:** Perform specific data structuring tasks.
   - **PostgreSQL:** Persists the final data and immutable audit events.

---

## PART 10 — LIMITATIONS (9:00 - 10:00)
**Conclude the video by speaking to the camera/mic:**
> "To conclude, I want to note that this is a technical demonstration. Production-grade OCR is not implemented because it was not required; we extract text directly from the digital files.
> 
> Furthermore, the AI risk assessment is preliminary. QA personnel must review AI-generated assessments, and this application does not replace approved pharmaceutical QMS/SOP processes."

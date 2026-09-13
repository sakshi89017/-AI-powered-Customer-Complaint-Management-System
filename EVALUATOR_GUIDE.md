# Evaluator Guide

Welcome to the AI-Powered Customer Complaint Management System! This guide is designed to help you quickly understand the project architecture, the problems it solves, and the technologies used.

## 1. What Problem This Solves
In the pharmaceutical industry, Quality Assurance (QA) personnel often manually transcribe customer complaints from diverse sources (emails, PDFs, verbal reports) into complex QMS (Quality Management System) databases. This manual data entry is slow, prone to errors, and delays critical risk assessments that might affect patient safety.

## 2. What the Customer Complaint Module Does
The Customer Complaint module is the entry point for post-market surveillance. It logs product defects (e.g., discolored pills, damaged packaging) so that QA can investigate the root cause, determine if a batch recall is necessary, and maintain regulatory compliance (like 21 CFR Part 11).

## 3. Why AI is Useful Here
AI excels at natural language understanding and unstructured data extraction. By using an AI assistant, QA personnel can simply state the complaint or upload a document, and the AI will structure the data automatically. This eliminates manual transcription and provides an instant, preliminary risk assessment to prioritize critical issues.

## 4. How the AI Co-Pilot Works
The AI Co-Pilot acts as an intelligent assistant sitting alongside the complaint form. Users chat with the Co-Pilot or upload files. The Co-Pilot uses LangGraph to determine the user's intent, executes the appropriate tool to extract the structured data, and then patches that data directly into the application's Redux state, visually updating the form in real-time.

## 5. How LangGraph is Used
LangGraph orchestrates the AI workflow. Instead of a single static LLM call, LangGraph routes the user's input through a directed graph. It detects the user's intent (e.g., logging a new complaint vs. editing an existing one) and selects the specific Python tool required to handle that task.

## 6. How Redux is Used
Redux Toolkit manages the global state of the frontend. The `activeComplaint` state acts as the single source of truth. When the AI extracts data, Redux merges the AI's differential updates with the existing form data. The React UI instantly reacts to these Redux state changes.

## 7. How FastAPI is Used
FastAPI provides a high-performance, asynchronous Python backend. It handles all RESTful routing, validates data using Pydantic schemas (ensuring the AI doesn't corrupt the database with malformed data), and serves as the secure bridge between the frontend, the PostgreSQL database, and the external Groq LLM API.

## 8. How PostgreSQL is Used
PostgreSQL is the persistent, relational database. It stores the final structured complaints and maintains an immutable Audit Trail (`complaint_events` table). Every time a complaint is saved, PostgreSQL records exactly which fields changed, what the old values were, and what the new values are.

## 9. How Groq / gemma2-9b-it is Used
Groq provides ultra-fast LLM inference. The application utilizes the open-weight `gemma2-9b-it` model (or `llama-3.3-70b-versatile`). The LLM is responsible for reading the natural language, determining the structured JSON output requested by our Pydantic schemas, and generating the preliminary risk assessments.

## 10. The Three AI Tools

| Tool | Input | What it does | Output |
|------|-------|--------------|--------|
| **Log Complaint** | Natural-language complaint | → extracts information<br>→ populates form<br>→ initial risk assessment | Structured JSON matching the Complaint schema |
| **Edit Complaint** | Natural-language correction | → changes only requested fields<br>→ reassesses risk when needed | Differential JSON patch (only changed fields) |
| **Document Extraction** | PDF / email / text | → extracts complaint information<br>→ populates form<br>→ performs risk assessment | Structured JSON merged with existing state |

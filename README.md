# AI-Powered Book Summarizer Pipeline
An end-to-end event-driven pipeline that automates the extraction and summarization of text from PDF or TXT files using Flask, Google Cloud Platform (GCP), n8n, and OpenAI.

## Project Architecture

1. **Frontend UI (Flask):** Provides a sleek web interface for users to upload documents.
2. **Storage (Google Drive / GCP):** Flask utilizes a GCP Service Account to seamlessly push uploaded files directly into a Google Drive folder (`Input_Uploads`).
3. **Orchestration (n8n):** A low-code automation workflow listens for new files in the Drive folder, downloads them, extracts the text, and chunks the content to manage LLM token limits.
4. **AI Processing (OpenAI):** The chunks are sent to OpenAI (e.g., GPT-4o-mini) for summarization and insight extraction.
5. **Output:** The compiled summary is saved as a Markdown file back to Google Drive (`Processed_Summaries`).

## Repository Structure

* `app.py`: The Flask web application entry point.
* `templates/index.html`: The frontend UI.
* `requirements.txt`: Python dependencies.
* `n8n_custom_scripts.js`: JavaScript logic used in the n8n code nodes for chunking and formatting.

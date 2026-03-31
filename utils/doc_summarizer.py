# utils/doc_summarizer.py

import os
import tempfile
from transformers import pipeline
from PyPDF2 import PdfReader
os.environ["TRANSFORMERS_CACHE"] = "/tmp"

# Initialize summarization model (replace with Granite later if needed)
summarizer = pipeline("summarization", model="sshleifer/tiny-bart")

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        return full_text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

def summarize_document(file):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        text = extract_text_from_pdf(tmp_path)
        if not text:
            return "⚠️ Could not extract any text from the document."

        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
        summaries = []
        for chunk in chunks:
            summary = summarizer(chunk, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
            summaries.append(summary)

        final_summary = "\n".join(summaries)
        os.remove(tmp_path)
        return f"📄 **Summary:**\n{final_summary}"
    except Exception as e:
        return f"⚠️ Error summarizing document: {str(e)}"

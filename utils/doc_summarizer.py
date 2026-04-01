from PyPDF2 import PdfReader
import tempfile
import os
import re
from collections import Counter


def extract_text(file):
    if file.type == "application/pdf":
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        reader = PdfReader(tmp_path)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content

        os.remove(tmp_path)
    else:
        text = file.read().decode("utf-8")

    return text


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text


def score_sentences(text):
    sentences = text.split(".")
    words = text.lower().split()

    word_freq = Counter(words)

    sentence_scores = {}

    for sentence in sentences:
        for word in sentence.lower().split():
            if word in word_freq:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_freq[word]
                else:
                    sentence_scores[sentence] += word_freq[word]

    return sentence_scores


def summarize_document(file):
    try:
        text = extract_text(file)
        text = clean_text(text)

        if not text.strip():
            return "No readable content found."

        sentence_scores = score_sentences(text)

        # Get top 3 sentences
        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:3]

        summary = ". ".join(top_sentences)

        return summary.strip()

    except Exception as e:
        return f"Error: {str(e)}"

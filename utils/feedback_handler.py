import re

CATEGORIES = {
    "Sanitation Department": ["garbage", "waste", "trash", "dirty"],
    "Traffic Department": ["traffic", "jam", "signal", "road block"],
    "Water Department": ["water", "leak", "pipe", "drain"],
    "Power Department": ["electricity", "power", "current", "voltage"],
    "Environmental Board": ["pollution", "smoke", "air", "noise"]
}


def clean_text(text):
    return re.sub(r'\s+', ' ', text.lower())


def summarize_text(text):
    sentences = text.split(".")
    return sentences[0].strip()


def classify_feedback(text):
    scores = {dept: 0 for dept in CATEGORIES}

    for dept, keywords in CATEGORIES.items():
        for word in keywords:
            if word in text:
                scores[dept] += 1

    # pick highest score
    best_match = max(scores, key=scores.get)

    if scores[best_match] == 0:
        return "General Support"

    return best_match


def detect_priority(text):
    urgent_words = ["urgent", "immediately", "danger", "accident"]

    for word in urgent_words:
        if word in text:
            return "High Priority"

    return "Normal Priority"


def handle_feedback(issue_text):
    if not issue_text.strip():
        return "Please enter a valid issue."

    cleaned = clean_text(issue_text)

    summary = summarize_text(issue_text)
    department = classify_feedback(cleaned)
    priority = detect_priority(cleaned)

    return (
        f"Summary: {summary}\n"
        f"Department: {department}\n"
        f"Priority: {priority}"
    )

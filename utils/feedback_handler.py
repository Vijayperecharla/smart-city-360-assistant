CATEGORIES = {
    "garbage": "Sanitation Department",
    "traffic": "Traffic Department",
    "water": "Water Department",
    "noise": "Noise Control",
    "electricity": "Power Department",
    "pollution": "Environmental Board"
}

def classify_feedback(text):
    for keyword in CATEGORIES:
        if keyword in text.lower():
            return CATEGORIES[keyword]
    return "General Support"

def handle_feedback(issue_text):
    if not issue_text.strip():
        return "Please enter a valid issue."

    summary = issue_text.split(".")[0]
    department = classify_feedback(issue_text)

    return f"Summary: {summary}\nRouted to: {department}"

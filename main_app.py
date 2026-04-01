import streamlit as st
from utils.feedback_handler import handle_feedback
from utils.doc_summarizer import summarize_document
from utils.eco_advisor import eco_advice
from utils.sensor_dashboard import get_city_metrics

st.set_page_config(page_title="Smart City 360°", layout="wide")

st.title("🏙️ Smart City 360° Assistant")
st.markdown("Use the tabs below to interact with various smart city modules.")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "City Health Dashboard",
    "Citizen Feedback System",
    "Document Summarization",
    "Eco Advice Assistant"
])

# TAB 1
with tab1:
    st.subheader("Real-Time Metrics")
    if st.button("Refresh Metrics"):
        metrics = get_city_metrics()
    
        # Convert to dictionary
        data = {}
        for line in metrics.split("\n"):
            key, value = line.split(":")
            data[key.strip()] = value.strip()
    
        # Display as columns (cards style)
        col1, col2, col3 = st.columns(3)
    
        keys = list(data.keys())
    
        for i, key in enumerate(keys):
            with [col1, col2, col3][i % 3]:
                st.metric(label=key, value=data[key])
    
        # Optional chart (dummy visualization)
        st.subheader("City Metrics Overview")
        df = pd.DataFrame({
            "Metric": list(data.keys()),
            "Value": [i + 1 for i in range(len(data))]
        })
    
        st.bar_chart(df.set_index("Metric"))

# TAB 2
with tab2:
    st.subheader("Report a City Issue")
    issue = st.text_area("Describe the issue (e.g. water leak, traffic jam)")
    
    if st.button("Submit Feedback"):
        result = handle_feedback(issue)
        st.success("Feedback Processed:")
        st.text(result)

# TAB 3
with tab3:
    st.subheader("Summarize a Document")
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

    if uploaded_file and st.button("Summarize"):
        with st.spinner("Summarizing..."):
            summary = summarize_document(uploaded_file)
            st.success("Summary:")
            st.write(summary)

# TAB 4
with tab4:
    st.subheader("Eco-friendly Suggestions")
    query = st.text_input("Ask something like 'How to save electricity?'")

    if st.button("Get Advice"):
        result = eco_advice(query)
        st.success("Eco Advice:")
        st.text(result)

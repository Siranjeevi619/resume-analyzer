import streamlit as st
import requests
import uuid

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Resume Chat Assistant",
    layout="wide"
)

st.title("🤖 Resume Chat Assistant")

# -----------------------------
# Session State
# -----------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar – Resume Upload
# -----------------------------
with st.sidebar:
    st.header("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload PDF / DOCX",
        type=["pdf", "docx"]
    )

    if uploaded_file and st.button("Process Resume"):
        with st.spinner("Processing resume..."):
            files = {
                "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
            }

            res = requests.post(
                f"{API_URL}/resume/upload",
                files=files
            )

            if res.status_code == 200:
                st.session_state.resume_text = res.json()["raw_text"]
                st.session_state.messages = []
                st.success("Resume uploaded successfully ✅")
            else:
                st.error("Failed to process resume")

    st.divider()
    st.subheader("📌 Optional Job Description")
    job_description = st.text_area(
        "Paste JD (optional)",
        height=150
    )

# -----------------------------
# Chat Area
# -----------------------------
if not st.session_state.resume_text:
    st.info("👈 Upload your resume to start chatting")
    st.stop()

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input (bottom input box)
user_input = st.chat_input("Ask about your resume...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call backend
    payload = {
        "session_id": st.session_state.session_id,
        "resume_text": st.session_state.resume_text,
        "job_description": job_description,
        "question": user_input
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                f"{API_URL}/resume/chat",
                json=payload
            )

            if response.status_code == 200:
                answer = response.json()["answer"]
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            else:
                st.error("Error from backend")

import streamlit as st
import requests
import json
import os
from datetime import datetime

st.set_page_config(page_title="RAG Chat", layout="wide")

st.title("📚 Ask My Cloud Computing Docs")

HISTORY_FILE = "history.json"

# Load history from file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# Save history to file
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = load_history()

# Sidebar
st.sidebar.title("🕘 Chat History")

if st.sidebar.button("🗑 Clear History"):
    st.session_state.history = []
    save_history([])

for i, chat in enumerate(st.session_state.history):
    st.sidebar.markdown(f"🕒 {chat['time']}")
    st.sidebar.markdown(f"**Q{i+1}:** {chat['question']}")
    st.sidebar.markdown(f"➡️ {chat['answer'][:100]}...")
    st.sidebar.markdown("---")

# Input
user_input = st.text_input("Ask a question:")

if st.button("Ask") and user_input:
    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={"question": user_input}
    )

    data = response.json()

    # Save to history
    st.session_state.history.append({
        "question": user_input,
        "answer": data["answer"],
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_history(st.session_state.history)

    # Display answer
    st.subheader("Answer:")
    st.write(data["answer"])

    if "latency" in data:
        st.caption(f"⏱ Latency: {data['latency']:.2f} sec")
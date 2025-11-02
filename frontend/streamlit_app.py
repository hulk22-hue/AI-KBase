import streamlit as st
import requests
import json
from io import BytesIO

# --- Backend base URL ---
API_BASE = "http://localhost:8000/api"

st.set_page_config(page_title="AI Knowledge Base", page_icon="🧠", layout="wide")
st.title("🧠 AI-Powered Knowledge Base Search & Enrichment")

session_defaults = {
    "last_query": None,
    "query_result": None,
    "query_error": None,
    "rating_status": None,
}
for key, value in session_defaults.items():
    st.session_state.setdefault(key, value)
    
st.sidebar.header("📄 Upload Documents")

uploaded_files = st.sidebar.file_uploader("Upload multiple documents", accept_multiple_files=True)

if uploaded_files and st.sidebar.button("Upload"):
    for file in uploaded_files:
        with st.spinner(f"Uploading {file.name}..."):
            files = {"file": (file.name, BytesIO(file.read()), file.type or "application/octet-stream")}
            res = requests.post(f"{API_BASE}/upload", files=files)
            if res.status_code == 200:
                st.sidebar.success(f"Uploaded: {file.name}")
            else:
                st.sidebar.error(f"Failed: {file.name}")

st.sidebar.markdown("---")

st.subheader("💬 Ask a question about your documents")
user_query = st.text_input("Enter your query:")

if st.button("Submit Query") and user_query:
    with st.spinner("Thinking..."):
        try:
            res = requests.post(f"{API_BASE}/query", json={"text": user_query})
        except requests.RequestException as exc:
            st.session_state["query_result"] = None
            st.session_state["query_error"] = f"Request error: {exc}"
        else:
            if res.status_code == 200:
                st.session_state["query_result"] = res.json()
                st.session_state["last_query"] = user_query
                st.session_state["query_error"] = None
                st.session_state["rating_status"] = None
            else:
                st.session_state["query_result"] = None
                st.session_state["query_error"] = (
                    res.text or f"Query failed with status {res.status_code}"
                )
            
if st.session_state["query_error"]:
    st.error(st.session_state["query_error"])
    
data = st.session_state.get("query_result")
last_query = st.session_state.get("last_query")

if data:
    st.markdown("### 🧩 Answer")
    st.write(data.get("answer", "No answer generated."))

    st.markdown("### 🔍 Completeness Check")
    completeness = data.get("completeness", "N/A")
    color = "🟢" if completeness == "HIGH" else "🟠" if completeness == "MEDIUM" else "🔴"
    st.write(f"{color} **{completeness}**")

    if data.get("missing_info"):
        st.markdown("**Missing Info:**")
        for info in data["missing_info"]:
            st.markdown(f"- {info}")

    if data.get("enrichment_actions"):
        st.markdown("### 💡 Suggested Enrichment Actions")
        for e in data["enrichment_actions"]:
            st.markdown(f"- `{e['type']}` → {e['label']}")

    if data.get("auto_fetched_data"):
        st.markdown("### 🌐 Auto-Fetched Data")
        for f in data["auto_fetched_data"]:
            st.markdown(f"- **{f['query']}**: {f['data']}")

    st.markdown("---")
    st.markdown("### ❤️ Rate this Answer")
    col1, col2 = st.columns(2)

    like_clicked = col1.button("👍 Like", key="like_btn")
    dislike_clicked = col2.button("👎 Dislike", key="dislike_btn")

    if like_clicked or dislike_clicked:
        rating = "like" if like_clicked else "dislike"
        payload = {
            "question": last_query or "",
            "answer": data.get("answer", ""),
            "rating": rating,
            "comments": f"{rating.title()}d via Streamlit UI",
        }
        try:
            response = requests.post(f"{API_BASE}/rate", json=payload)
            if response.status_code == 200:
                st.session_state["rating_status"] = (
                    "success",
                    "Feedback recorded — Thanks!" if rating == "like" else "Feedback recorded — we’ll improve this!",
                )
            else:
                st.session_state["rating_status"] = (
                    "error",
                    response.text or f"Feedback failed with status {response.status_code}",
                )
        except requests.RequestException as exc:
            st.session_state["rating_status"] = ("error", f"Feedback error: {exc}")

# --- Display feedback message (persistent) ---
if st.session_state["rating_status"]:
    status, message = st.session_state["rating_status"]
    if status == "success":
        st.success(message)
    else:
        st.error(message)

# --- Show errors if any ---
if st.session_state["query_error"]:
    st.error(st.session_state["query_error"])
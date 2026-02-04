import streamlit as st
import ollama
from firebase import get_db
from firebase_admin import firestore

db = get_db()

def get_all_conversations():
    convos = db.collection("conversations") \
               .order_by("created_at", direction=firestore.Query.DESCENDING) \
               .stream()

    return [
        {"convo_id": convo.id, **convo.to_dict()}
        for convo in convos
    ]

def load_messages(convo_id):
    msgs = db.collection("conversations") \
             .document(convo_id) \
             .collection("messages") \
             .order_by("timestamp") \
             .stream()
    return [m.to_dict() for m in msgs]

def format_conversation(convo_id):
    messages = load_messages(convo_id)
    return "\n".join(
        f"{m.get('role', 'Unknown')}: {m.get('original_text', '')}"
        for m in messages
    )


def summarize_conversation(convo_id):
    conversation_text = format_conversation(convo_id)

    if not conversation_text.strip():
        return "No messages found in this conversation."

    prompt = f"""
You are a medical assistant.

Summarize the following doctor-patient conversation.
Extract and clearly list:
- Symptoms
- Diagnosis (if any)
- Medications
- Follow-up instructions

Be concise and factual. Do NOT hallucinate.

Conversation:
{conversation_text}
"""

    response = ollama.chat(
        model="mistral:latest",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

st.title("🧠 Chat Summarizer")
st.info(
    "AI-powered summarization is disabled in this deployed demo. "
    "This feature uses a locally hosted LLM (Ollama) to preserve medical data privacy "
    "and requires local execution."
)
conversations = get_all_conversations()

if not conversations:
    st.warning("No conversations found.")
else:
    convo_map = {
        f"{c['convo_id'][:8]} | {c.get('created_at', 'N/A')}": c["convo_id"]
        for c in conversations
    }

    selected = st.selectbox(
        "Select conversation",
        list(convo_map.keys())
    )

    if st.button("Generate Summary", disabled=True):
        with st.spinner("Generating summary..."):
            summary = summarize_conversation(convo_map[selected])
        st.success(summary)

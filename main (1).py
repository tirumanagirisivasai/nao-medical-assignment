import streamlit as st
from deep_translator import GoogleTranslator
import whisper
import tempfile
import os
from firebase_admin import credentials, firestore
from firebase import get_db
db = get_db()
# 1. Page Configuration
st.set_page_config(page_title="Doctor–Patient Translator", layout="wide")

st.markdown("""
<style>
    .bubble { padding: 15px; border-radius: 15px; margin: 10px 0; width: fit-content; max-width: 80%; }
    .bubble-doc { background-color: #e6f2ff; border-left: 5px solid #007bff; }
    .bubble-pat { background-color: #f2f2f2; border-left: 5px solid #28a745; margin-left: auto; }
</style>
""", unsafe_allow_html=True)

# 2. Initialization & Models
if "chat" not in st.session_state:
    st.session_state.chat = []
if "last_processed_audio" not in st.session_state:
    st.session_state.last_processed_audio = None

@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

model = load_whisper()


# 3. Helper Functions
def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]

def translate_text(text, src, tgt):
    return GoogleTranslator(source=src, target=tgt).translate(text)

def add_message(role, original, translated):
    st.session_state.chat.append({
        "role": role,
        "original": original,
        "translated": translated
    })
import uuid
from datetime import datetime

def create_conversation():
    convo_id = str(uuid.uuid4())
    db.collection("conversations").document(convo_id).set({
        "created_at": datetime.utcnow(),
        "summary": ""
    })
    return convo_id

def save_message(convo_id, data):
    db.collection("conversations") \
      .document(convo_id) \
      .collection("messages") \
      .add({
          **data,
          "timestamp": firestore.SERVER_TIMESTAMP
      })


if "convo_id" not in st.session_state:
    st.session_state.convo_id = create_conversation()

# 4. UI Sidebar & Layout
st.title("🩺 Doctor–Patient Translator")

with st.sidebar:
    st.header("Settings")
    doctor_lang = st.selectbox("Doctor's Language", ["en", "fr", "de", "es", "hi", "zh-CN"], index=0)
    patient_lang = st.selectbox("Patient's Language", ["en", "fr", "de", "es", "hi", "zh-CN"], index=4)
    if st.button("Clear Conversation"):
        st.session_state.chat = []
        st.rerun()

# 5. Display Chat History
chat_container = st.container()
with chat_container:
    for msg in st.session_state.chat:
        style = "bubble-doc" if msg["role"] == "Doctor" else "bubble-pat"
        st.markdown(f"""
            <div class="bubble {style}">
                <b>{msg['role']}:</b><br>
                <small style="color: grey;">{msg['original']}</small><br>
                <strong>{msg['translated']}</strong>
            </div>
        """, unsafe_allow_html=True)

# 6. Input Section
st.divider()
current_role = st.radio("Who is speaking?", ["Doctor", "Patient"], horizontal=True)

# Logic: Determine Source and Target based on who is speaking
active_src = doctor_lang if current_role == "Doctor" else patient_lang
active_tgt = patient_lang if current_role == "Doctor" else doctor_lang

user_text = st.chat_input("Type your message here...")
audio = st.audio_input("Or record your voice")

# 7. Processing Text Input
if user_text:
    translated = translate_text(user_text, active_src, active_tgt)
    add_message(current_role, user_text, translated)
    save_message(
    st.session_state.convo_id,
    {
        "role": current_role,
        "original_text": user_text,
        "translated_text": translated,
        "input_language": active_src,
        "output_language": active_tgt
    }
)

    st.rerun()

# 8. Processing Audio Input (With Loop Protection)
if audio:
    audio_hash = hash(audio.getbuffer().tobytes())

    if st.session_state.last_processed_audio != audio_hash:
        with st.spinner("Processing speech..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio.getbuffer())
                tmp_path = f.name
            
            # Transcription
            raw_text = transcribe_audio(tmp_path)
            
            # Translation
            translated_text = translate_text(raw_text, active_src, active_tgt)
            
            # Save and Update State
            add_message(current_role, raw_text, translated_text)
            save_message(
                        st.session_state.convo_id,
                        {
                            "role": current_role,
                            "original_text": raw_text,
                            "translated_text": translated_text,
                            "input_language": active_src,
                            "output_language": active_tgt
                        }
                    )

            st.session_state.last_processed_audio = audio_hash
            
            # Cleanup
            os.remove(tmp_path)
            st.rerun()

other_page_url = "https://google.com"
    
    # Custom HTML Button Link
st.markdown(f"""
    <a href="{other_page_url}" target="_blank" style="text-decoration: none;">
        <div style="
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            text-align: center;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            border: none;">
            Go to Summarizer page ➔
        </div>
    </a>
""", unsafe_allow_html=True)
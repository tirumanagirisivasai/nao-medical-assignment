# Doctor–Patient Real-Time Translation & Conversation Assistant

## Project Overview

This project is a Streamlit-based web application designed to facilitate real-time communication between doctors and patients who speak different languages. The application supports multilingual text and speech translation, persistent conversation logging, and post-conversation analysis through AI-generated summaries.

The primary goal of this project is to demonstrate an end-to-end applied AI system involving speech recognition, translation, NoSQL data storage, and LLM-based summarization, with a strong emphasis on privacy-aware design choices suitable for healthcare use cases.

---

## Features Attempted & Completed

### Core Features (Completed)

- **Real-Time Doctor–Patient Translation**
  - Supports two roles: Doctor and Patient
  - Automatic translation based on the active speaker
  - Multilingual support (e.g., English, Hindi, French, German, etc.)

- **Text Chat Interface**
  - Clean, chat-style UI built using Streamlit
  - Clear visual distinction between Doctor and Patient messages

- **Audio Recording & Speech-to-Text**
  - Audio recording directly from the browser
  - Speech transcription using Whisper (CPU-based)
  - Transcribed speech is translated and added to the conversation flow

- **Conversation Logging & Persistence**
  - Conversations stored in **Firebase Firestore (NoSQL)**
  - Messages stored as subcollections with timestamps
  - Conversation data persists beyond active sessions

- **Conversation Retrieval**
  - Ability to load previous conversations using conversation IDs
  - Chronological message rendering

- **AI-Powered Conversation Summary (Local Mode)**
  - Generates concise medical summaries highlighting:
    - Symptoms
    - Diagnoses
    - Medications
    - Follow-up instructions
  - Implemented using a locally hosted LLM via **Ollama**

---

## Tech Stack Used

### Frontend / UI
- **Streamlit** – Web application framework

### Speech & Language
- **Whisper (OpenAI)** – Speech-to-text transcription (CPU mode)
- **Deep Translator (GoogleTranslator)** – Text translation

### Backend & Storage
- **Firebase Firestore** – NoSQL database for conversation and message storage
- **Firebase Admin SDK** – Secure backend access

### AI / LLM
- **Ollama (Local LLM runtime)** – Used for privacy-preserving medical summarization

### DevOps / Deployment
- **Docker** – Containerized application setup
- **Python 3.10**

---

## 🤖 AI Tools & Resources Leveraged

- **Whisper** for speech recognition
- **Google Translate (via Deep Translator)** for multilingual text translation
- **Local LLMs (Mistral / LLaMA via Ollama)** for conversation summarization
- **Prompt engineering** for extracting structured medical information

---

## Known Limitations & Trade-offs

- **AI Summarization Disabled in Public Deployment**
  - The summarization feature relies on a locally hosted LLM (Ollama)
  - Free cloud hosting platforms do not support persistent local model servers
  - As a result, summarization is available **only in local execution mode**
  - The deployed demo disables this feature intentionally

- **No Full-Text Search**
  - Firestore does not natively support full-text search
  - Keyword-based search is basic
  - In a production setup, services like Algolia or Elasticsearch would be integrated

- **No Authentication / Role-Based Access Control**
  - User authentication (Doctor vs Patient login) is not implemented
  - This was intentionally scoped out for simplicity

- **CPU-Only Inference**
  - Whisper and local LLMs run on CPU
  - Performance may be slower on low-memory systems

- **Free-Tier Hosting Constraints**
  - Inactive cloud instances may automatically shut down
  - This behavior is expected and not bypassed intentionally

---

## Design Decisions & Trade-offs

- Chose **local LLM (Ollama)** over cloud APIs to:
  - Preserve data privacy for healthcare conversations
  - Avoid dependency on paid APIs
- Used **Firestore NoSQL schema** for flexibility and scalability
- Modularized features to allow:
  - Local-only enhancements
  - Easy future cloud migration

---

## Future Improvements

- Add authentication and role-based access
- Integrate medical entity highlighting (NER)
- Enable scalable full-text search
- Add encrypted audio storage (Firebase Storage)
- Optional fallback to cloud-based LLMs when available

---

## Notes

This project is designed as a **demonstration of applied AI system design** rather than a production-ready medical system. All medical summaries are AI-generated and should not be used for clinical decision-making.

---

## Author
Siva Sai Prasad Tirumanagiri

Developed as part of an AI Engineer Intern assignment / project demonstration.

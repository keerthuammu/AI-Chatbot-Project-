import streamlit as st
import os
from groq import Groq

# Page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot")

# Load API key (from environment or Streamlit secrets)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except:
        st.error("⚠️ Please set GROQ_API_KEY in Streamlit secrets or environment variables")
        st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Save and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Typing...")

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=200
            )

            reply = response.choices[0].message.content

        except Exception as e:
            reply = f"⚠️ Error: {e}"

        placeholder.markdown(reply)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": reply})
import streamlit as st
import os
from groq import Groq


st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except:
        st.error("⚠️ Please set GROQ_API_KEY in environment variables or Streamlit secrets")
        st.stop()

client = Groq(api_key=GROQ_API_KEY)


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display instantly
    st.chat_message("user").write(user_input)

    # Assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Typing...")

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # ✅ working model
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=200
            )

            reply = response.choices[0].message.content

        except Exception as e:
            reply = "⚠️ Error: " + str(e)

        placeholder.markdown(reply)

    # Save bot reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
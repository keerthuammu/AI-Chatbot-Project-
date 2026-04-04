import streamlit as st
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

# Store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show user message instantly
    st.chat_message("user").write(user_input)

    # Show typing animation
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Typing...")

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant", # ✅ updated model
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content

        except Exception as e:
            reply = "⚠️ Error: " + str(e)

        # Replace typing with real response
        message_placeholder.markdown(reply)

    # Save bot response
    st.session_state.messages.append({"role": "assistant", "content": reply})
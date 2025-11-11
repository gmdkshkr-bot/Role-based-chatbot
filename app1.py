import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="My Chatbot", page_icon="🤖")

st.title("🤖 My OpenAI Chatbot")

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful, concise assistant."}
    ]

# Render chat history
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# Input box
user_input = st.chat_input("Ask something...")

if user_input:
    # Add user msg
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Call OpenAI
    response = client.responses.create(
        model="gpt-4o-mini",
        input=st.session_state["messages"],
        max_output_tokens=500,
        temperature=0.5
    )

    bot_reply = response.output[0].content[0].text

    # Add assistant msg
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)

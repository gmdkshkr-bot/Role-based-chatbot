import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="My Chatbot", page_icon="🤖")
st.title("🤖 My OpenAI Chatbot")

# --- Step 1: Ask for API key ---
api_key = st.text_input(
    "Enter your OpenAI API Key",
    type="password",
    help="Your key will only be stored in session memory."
)

if not api_key:
    st.warning("Please enter your API key to start.")
    st.stop()

# Create client dynamically
client = OpenAI(api_key=api_key)

# --- Step 2: Setup message history ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Render previous messages
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# --- Step 3: Chat input ---
user_input = st.chat_input("Ask something...")

if user_input:
    # Save user message
    st.session_state["messages"].append(
        {"role": "user", "content": user_input}
    )
    st.chat_message("user").write(user_input)

    # Call OpenAI
    response = client.responses.create(
        model="gpt-4o-mini",
        input=st.session_state["messages"],
        temperature=0.4,
        max_output_tokens=500,
    )

    bot_reply = response.output[0].content[0].text

    # Save and render assistant message
    st.session_state["messages"].append(
        {"role": "assistant", "content": bot_reply}
    )
    st.chat_message("assistant").write(bot_reply)

# Optional: keep short memory
st.session_state["messages"] = st.session_state["messages"][-6:]

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Creative Role Chatbot", page_icon="🎨")
st.title("🎭 Creative Role-Based Chatbot")

# --- STEP 1: API key input ---
api_key = st.text_input("Enter your OpenAI API Key", type="password")
if not api_key:
    st.warning("Please enter your API key to begin.")
    st.stop()

client = OpenAI(api_key=api_key)

# --- STEP 2: Define creative/art roles ---
creative_roles = {
    "Art Historian": "You are an art historian. Provide context, timelines, and significance of artworks and movements.",
    "Painter": "You are a professional painter. Give detailed painting techniques, tips, and color theory explanations.",
    "Sculptor": "You are an experienced sculptor. Discuss materials, tools, and methods for creating sculptures.",
    "Art Critic": "You are an art critic. Offer thoughtful analysis and interpretation of artworks with constructive insight.",
    "Museum Curator": "You are a museum curator. Give advice about exhibitions, curation strategies, and art presentation.",
    "Video Director": "You are a professional video director. Advise on directing, cinematography, scene composition, and storytelling.",
    "Fashion Stylist": "You are a fashion stylist. Give tips on outfits, colors, trends, and styling for different occasions or photoshoots.",
    "Acting Coach": "You are an acting coach. Provide guidance on acting techniques, character development, and performance skills.",
    "Dance Instructor": "You are a dance instructor. Give instructions on techniques, choreography, and improving style for different dance forms."
}

selected_role = st.selectbox("Choose your creative assistant role:", list(creative_roles.keys()))

# --- STEP 3: Initialize conversation memory ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": creative_roles[selected_role]}
    ]

# Reset memory if role changes
if "last_role" not in st.session_state:
    st.session_state["last_role"] = selected_role

if selected_role != st.session_state["last_role"]:
    st.session_state["messages"] = [
        {"role": "system", "content": creative_roles[selected_role]}
    ]
    st.session_state["last_role"] = selected_role

# --- STEP 4: Display chat history ---
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# --- STEP 5: Chat input ---
user_input = st.chat_input("Ask your question...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # OpenAI API call
    response = client.responses.create(
        model="gpt-4o-mini",
        input=st.session_state["messages"],
        temperature=0.5,
        max_output_tokens=500,
    )

    bot_reply = response.output[0].content[0].text

    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)

# Optional: keep only last 8 messages
st.session_state["messages"] = st.session_state["messages"][-8:]

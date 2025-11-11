import streamlit as st
from openai import OpenAI
import time

st.set_page_config(page_title="Creative Role Chatbot", page_icon="🎨")
st.title("🎭 Creative Role-Based Chatbot (User API Key)")

# --- STEP 1: User enters their API key ---
api_key = st.text_input(
    "Enter your OpenAI API Key",
    type="password",
    help="Your key is only stored in session memory and never saved permanently."
)
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

# --- STEP 4: Rate limiting per user ---
if "last_message_time" not in st.session_state:
    st.session_state["last_message_time"] = 0

RATE_LIMIT_SEC = 10  # one message per 10 seconds

# --- STEP 5: Display previous messages ---
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# --- STEP 6: Chat input ---
user_input = st.chat_input("Ask your question...")

if user_input:
    now = time.time()
    if now - st.session_state["last_message_time"] < RATE_LIMIT_SEC:
        st.warning(
            f"Please wait {int(RATE_LIMIT_SEC - (now - st.session_state['last_message_time']))}s before sending another message."
        )
        st.stop()

    st.session_state["last_message_time"] = now
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # --- STEP 7: Use cheaper model (gpt-3.5-turbo) for free-tier ---
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["messages"],
            temperature=0.5,
            max_tokens=400,
        )

        bot_reply = response.choices[0].message.content

        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").write(bot_reply)
    except Exception as e:
        st.error(f"Error calling OpenAI API: {e}")

# --- STEP 8: Trim conversation memory intelligently ---
# Keep system + last 6 messages
st.session_state["messages"] = [st.session_state["messages"][0]] + st.session_state["messages"][-6:]

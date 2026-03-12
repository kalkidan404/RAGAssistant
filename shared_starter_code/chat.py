import streamlit as st
import requests
import os

st.set_page_config(page_title="AAU Assistant", page_icon="🎓")

# Custom CSS for black-and-gold theme
st.markdown("""
<style>
.stApp { 
    background-color: #0D0D0D;  /* Black background */
    color: #FFD700;             /* Gold default text */
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    background-color: #1A1A1A;  /* Dark bubble background */
    color: #FFD700;             /* Gold text in bubble */
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 10px;
}

/* Buttons */
.stButton>button {
    background-color: #FFD700;   /* Gold buttons */
    color: #0D0D0D;              /* Black text on buttons */
    border: none;
}

/* Input box */
.stTextInput>div>div>input {
    background-color: #1A1A1A;  /* Dark input box */
    color: #FFD700;              /* Gold input text */
    border: 1px solid #FFD700;   /* Optional gold border */
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 AAU General Assistant")

# --- CONFIGURATION ---
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/ask")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How can I help you today?"):
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call the FastAPI backend
    try:
        with st.spinner("Consulting AAU documents..."):
            response = requests.post(
                BACKEND_URL,
                json={"question": prompt},
                timeout=60
            )

        if response.status_code == 200:
            data = response.json()
            answer = data["answer"]

            # Show assistant message
            with st.chat_message("assistant"):
                st.markdown(answer)
            
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"Backend error: {response.status_code}")

    except Exception as e:
        st.error(f"Connection failed. Ensure FastAPI is running at {BACKEND_URL}")
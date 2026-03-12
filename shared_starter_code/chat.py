import streamlit as st
import requests
import os

st.set_page_config(page_title="AAU Assistant", page_icon="🎓")

# Custom CSS for black-and-gold theme
# Custom CSS for black-and-gold theme
st.markdown("""
<style>
/* 1. Global Background */
.stApp { 
    background-color: #000000 !important; 
}

/* 2. Force EVERY text element to Gold */
* {
    color: #FFD700 !important;
    font-family: 'sans-serif';
}

/* 3. Specifically target headers and titles */
h1, h2, h3, p, span, label, div {
    color: #FFD700 !important;
}

/* 4. Chat Input Box (Text you type) */
input, textarea {
    color: #FFD700 !important;
    -webkit-text-fill-color: #FFD700 !important;
    background-color: #1A1A1A !important;
}

/* 5. Chat Bubbles */
[data-testid="stChatMessage"] {
    background-color: #1A1A1A !important;
    border: 1px solid #FFD700 !important;
}

/* 6. Spinner/Loading Message */
.stSpinner > div > div {
    color: #FFD700 !important;
}

/* 7. Hide the default Streamlit footer/menu for a cleaner look */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

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
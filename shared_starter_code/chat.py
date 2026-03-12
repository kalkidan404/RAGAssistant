import streamlit as st
import requests
import os

st.set_page_config(page_title="AAU Assistant", page_icon="🎓")

# Custom CSS for the AAU dark theme
st.markdown("""
<style>
.stApp { 
    background-color: #2B0D3F; 
    color: white; 
}
[data-testid="stChatMessage"] {
    background-color: #3D125A;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 AAU General Assistant")

# --- CONFIGURATION ---
# Use environment variable for deployment, fallback to localhost for testing
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
    
    # 1. Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Call the FastAPI backend
    try:
        with st.spinner("Consulting AAU documents..."):
            response = requests.post(
                BACKEND_URL,
                json={"question": prompt},
                timeout=60 # Increased timeout for LLM processing
            )

        if response.status_code == 200:
            data = response.json()
            answer = data["answer"]

            # 3. Show assistant message and save to history
            with st.chat_message("assistant"):
                st.markdown(answer)
            
            st.session_state.messages.append({"role": "assistant", "content": answer})

        else:
            st.error(f"Backend error: {response.status_code}")

    except Exception as e:
        st.error(f"Connection failed. Ensure FastAPI is running at {BACKEND_URL}")

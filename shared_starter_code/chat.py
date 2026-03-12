import streamlit as st
from app import get_answer  # <--- THIS LINKS THE TWO FILES

st.set_page_config(page_title="AAU Assistant", page_icon="🎓")

# (Keep your Golden CSS here...)

st.title("🎓 AAU General Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Consulting AAU documents..."):
        # CALL THE BACKEND FILE DIRECTLY
        answer = get_answer(prompt, st.session_state.messages)
        
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

# -*- coding: utf-8 -*-
import streamlit as st
from ai_agent import get_response



st.set_page_config(page_title="Input Genius", page_icon="💬")

st.title("💬 Input Genius - Ein RAG-Agent")
st.write("Frage mich was")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
   


if prompt := st.chat_input("Stelle mir eine Frage..."):
    with st.spinner("Denke nach..."):
        with st.chat_message("user", avatar=None, width="content"):
            st.write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        thinking, response, result  = get_response(prompt)
        
        
        with st.chat_message("ai"):
            if thinking is None or response is None: 
                st.write(result)
                st.session_state.messages.append({"role": "ai", "content": result})
            else:
                st.markdown(
                f"<strong>Agent is thinking:</strong><p>{thinking}</p><br><strong>Agent is answering:</strong><p>{response}</p>",
                unsafe_allow_html=True
                )
                st.session_state.messages.append({"role": "ai", "content": response})



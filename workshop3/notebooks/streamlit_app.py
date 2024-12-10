import sys
from pathlib import Path

# Add the workshop3 directory to Python path
root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

import streamlit as st
from helpers.book_support_langchain import ByteChaptersLangChainBot, ConversationClosed

def initialize_chat():
    if "bot" not in st.session_state:
        st.session_state.bot = ByteChaptersLangChainBot()
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    st.title("ByteChapters Customer Support")
    
    initialize_chat()

    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("How can I help you today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
        with st.chat_message("assistant"):
            try:
                response = st.session_state.bot.chat(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except ConversationClosed as e:
                st.error(str(e))
                st.session_state.bot.reset()
                st.session_state.messages = []

    # Reset button
    if st.sidebar.button("Reset Conversation"):
        st.session_state.bot.reset()
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main() 
import sys
from pathlib import Path
import os

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
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input("OpenAI API Key (optional)", type="password")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            
        st.divider()
        
        if st.button("Reset Conversation"):
            st.session_state.bot.reset()
            st.session_state.messages = []
            st.rerun()
    
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
            except Exception as e:
                if "openai api key" in str(e).lower():
                    st.error("Please provide a valid OpenAI API key in the sidebar.")
                else:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 
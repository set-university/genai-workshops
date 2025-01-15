import streamlit as st
from main import NavigationApp
from utils.config import Config


@st.cache_resource
def initialize_app(model_path):
    return NavigationApp(model_path)


def main():
    st.title("Navigation Assistant")

    model_path = Config.MODEL_PATH
    here_api_key = Config.HERE_API_KEY

    if not model_path or not here_api_key:
        st.warning("Please enter the model path and API key in the sidebar to continue.")
        return

    app = initialize_app(model_path)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to know?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            response = app.process_query(prompt)
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.messages.append(
                {"role": "assistant", "content": f"I'm sorry, but an error occurred: {str(e)}"})


if __name__ == "__main__":
    main()

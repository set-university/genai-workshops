import streamlit as st

st.set_page_config(page_title="AI Analytics Dashboard", page_icon="📊", layout="wide")

if "df" not in st.session_state:
    st.session_state.df = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

pg = st.navigation([
    st.Page("pages/dashboard.py", title="Dashboard", icon="📊"),
    st.Page("pages/chat.py", title="Chat with Data", icon="💬"),
    st.Page("pages/editor.py", title="Data Editor", icon="✏️"),
])

pg.run()

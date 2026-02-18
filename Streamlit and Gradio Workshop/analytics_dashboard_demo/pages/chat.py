import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

st.title("💬 Chat with Your Data")

df = st.session_state.get("df")

if df is None:
    st.warning("Please upload data on the **Dashboard** page first.")
    st.stop()

st.caption(f"Dataset: {len(df)} rows, {len(df.columns)} columns — `{', '.join(df.columns[:8])}`{'...' if len(df.columns) > 8 else ''}")

SYSTEM_PROMPT = f"""You are a data analyst assistant. The user has a pandas DataFrame called `df` with these columns:
{chr(10).join(f'- {col} ({df[col].dtype})' for col in df.columns)}

First 3 rows:
{df.head(3).to_string()}

When the user asks a question about the data:
1. Write Python code using pandas (the df is already loaded) and optionally plotly.express (imported as px)
2. Put the code in a ```python code block
3. The code should print() any textual answers
4. For charts, assign the figure to a variable called `fig`
5. Keep code concise — no unnecessary comments

If the question is not about data, answer conversationally without code."""

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "result" in msg:
            st.markdown(msg["result"])
        if "fig" in msg:
            st.plotly_chart(msg["fig"], use_container_width=True)

if prompt := st.chat_input("Ask about your data..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for h in st.session_state.chat_history:
        messages.append({"role": h["role"], "content": h["content"]})

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True,
            max_tokens=1024,
        )
        response = st.write_stream(stream)

    assistant_msg = {"role": "assistant", "content": response}

    import re
    code_blocks = re.findall(r"```python\n(.*?)```", response, re.DOTALL)

    if code_blocks:
        code = code_blocks[0]
        try:
            import io
            from contextlib import redirect_stdout

            local_ns = {"df": df.copy(), "pd": pd, "px": px}
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exec(code, local_ns)

            printed = stdout.getvalue().strip()
            if printed:
                assistant_msg["result"] = f"```\n{printed}\n```"
                st.markdown(assistant_msg["result"])

            if "fig" in local_ns and local_ns["fig"] is not None:
                assistant_msg["fig"] = local_ns["fig"]
                st.plotly_chart(local_ns["fig"], use_container_width=True)

        except Exception as e:
            error_text = f"⚠️ Code execution error: `{e}`"
            assistant_msg["result"] = error_text
            st.error(error_text)

    st.session_state.chat_history.append(assistant_msg)

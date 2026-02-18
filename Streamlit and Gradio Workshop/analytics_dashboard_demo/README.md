# AI-Powered Analytics Dashboard (Streamlit)

A multi-page data analytics app with interactive visualizations, AI-powered Q&A, and inline data editing.

## What it does

Three pages connected by shared state:

1. **Dashboard** — Upload CSV (or use sample data), filter with sidebar controls, see key metrics, bar charts, and time-series plots. Auto-detects columns and data types.
2. **Chat with Data** — Ask questions in natural language ("Which product has the highest revenue?"). GPT-4o writes pandas code, executes it, and shows results/charts inline.
3. **Data Editor** — Edit any cell directly in the browser using `st.data_editor`. Add/remove rows, fix values, then apply changes across all pages.

## Why Streamlit?

Streamlit is the natural choice for this demo because:

- **`st.navigation` + `st.Page`** — native multi-page apps with shared session state. No routing library, no hacks. Each page is a simple Python file.
- **`st.data_editor`** — interactive spreadsheet-like editing in the browser. Edit cells, add rows, change types — built in, not a third-party widget.
- **`st.chat_input` / `st.chat_message`** — clean chat UI that integrates naturally into a data app (vs. Gradio where chat IS the app)
- **`st.session_state`** — data persists across pages and reruns without external storage
- **Data-app DNA** — Streamlit was built for dashboards and data exploration. Sidebar filters, metrics, Plotly charts, dataframes — all first-class citizens.

Gradio excels at wrapping a single ML model in a UI, but for a multi-page data application with navigation, shared state, and mixed UI paradigms (charts + tables + chat), Streamlit is purpose-built.

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your-key-here
streamlit run app.py
```

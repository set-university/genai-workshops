import streamlit as st

st.title("✏️ Data Editor")

df = st.session_state.get("df")

if df is None:
    st.warning("Please upload data on the **Dashboard** page first.")
    st.stop()

st.caption("Edit cells directly in the table below. Changes are reflected across all pages.")

edited = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
    key="data_editor",
)

col1, col2 = st.columns(2)

with col1:
    if st.button("Apply changes", type="primary"):
        st.session_state.df = edited
        st.success(f"Saved! DataFrame now has {len(edited)} rows.")

with col2:
    csv = edited.to_csv(index=False).encode("utf-8")
    st.download_button("Download edited CSV", csv, "edited_data.csv", "text/csv")

st.divider()
st.subheader("Quick Stats")

col_a, col_b, col_c = st.columns(3)
col_a.metric("Rows", len(edited))
col_b.metric("Columns", len(edited.columns))
col_c.metric("Missing values", int(edited.isna().sum().sum()))

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Dashboard")

uploaded = st.file_uploader("Upload a CSV file", type="csv", key="dash_upload")

if uploaded:
    st.session_state.df = pd.read_csv(uploaded)

df = st.session_state.df

if df is None:
    st.info("Upload a CSV to get started, or use the sample data below.")
    if st.button("Load sample data"):
        df = pd.read_csv("business_sales_data.csv")
        st.session_state.df = df

if df is not None:
    st.sidebar.header("Filters")

    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    filters = {}
    for col in categorical_cols:
        unique_vals = df[col].unique().tolist()
        selected = st.sidebar.multiselect(f"Filter by {col}", unique_vals, default=unique_vals, key=f"filter_{col}")
        filters[col] = selected

    filtered = df.copy()
    for col, vals in filters.items():
        filtered = filtered[filtered[col].isin(vals)]

    numeric_cols = filtered.select_dtypes(include="number").columns.tolist()

    st.subheader("Key Metrics")
    cols = st.columns(min(len(numeric_cols), 4))
    for i, col_name in enumerate(numeric_cols[:4]):
        with cols[i]:
            st.metric(col_name, f"{filtered[col_name].sum():,.2f}")

    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        st.subheader("Revenue by Category")
        cat_col = st.selectbox("Group by", categorical_cols, key="bar_group")
        num_col = st.selectbox("Measure", numeric_cols, key="bar_measure")
        agg = filtered.groupby(cat_col)[num_col].sum().reset_index()
        fig = px.bar(agg, x=cat_col, y=num_col, title=f"{num_col} by {cat_col}")
        st.plotly_chart(fig, use_container_width=True)

    date_cols = [c for c in df.columns if "date" in c.lower()]
    if date_cols and len(numeric_cols) > 0:
        st.subheader("Trend Over Time")
        date_col = date_cols[0]
        filtered[date_col] = pd.to_datetime(filtered[date_col], errors="coerce")
        trend_metric = st.selectbox("Metric", numeric_cols, key="trend_metric")

        if len(categorical_cols) > 0:
            color_col = st.selectbox("Color by", [None] + categorical_cols, key="trend_color")
        else:
            color_col = None

        if color_col:
            trend = filtered.groupby([date_col, color_col])[trend_metric].sum().reset_index()
        else:
            trend = filtered.groupby(date_col)[trend_metric].sum().reset_index()

        fig = px.line(trend, x=date_col, y=trend_metric, color=color_col,
                      title=f"{trend_metric} Over Time", markers=True)
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Raw Data")
    st.dataframe(filtered, use_container_width=True)

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered CSV", csv, "filtered_data.csv", "text/csv")

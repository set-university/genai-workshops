import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Business Sales Dashboard 📊")

# 1. Load Dataset
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Raw Data", df.head())

    # 2. Filters
    st.sidebar.header("Filters")
    product_filter = st.sidebar.multiselect("Select Product(s)", df["Product"].unique(), default=df["Product"].unique())
    region_filter = st.sidebar.multiselect("Select Region(s)", df["Region"].unique(), default=df["Region"].unique())
    
    filtered_df = df[(df["Product"].isin(product_filter)) & (df["Region"].isin(region_filter))]

    # 3. Aggregated Metrics
    st.write("### Key Metrics")
    total_revenue = filtered_df["Revenue"].sum()
    total_quantity = filtered_df["Quantity_Sold"].sum()
    st.metric("Total Revenue", f"${total_revenue:,.2f}")
    st.metric("Total Quantity Sold", f"{total_quantity:,}")

    # 4. Visualization - Revenue by Product
    st.write("### Revenue by Product")
    revenue_by_product = filtered_df.groupby("Product")["Revenue"].sum().reset_index()
    fig_product = px.bar(
        revenue_by_product, 
        x="Product", 
        y="Revenue", 
        title="Revenue by Product", 
        labels={"Revenue": "Total Revenue", "Product": "Product"}
    )
    st.plotly_chart(fig_product)

    # 5. Visualization - Interactive Revenue Over Time with Product Selection
    st.write("### Revenue Over Time by Product")

    # Convert 'Date' to datetime and filter DataFrame
    filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])

    # Sidebar multi-select for product filtering
    products_available = filtered_df["Product"].unique()
    selected_products = st.multiselect(
        "Select Product(s) to Display",
        options=products_available,
        default=products_available  # Show all products by default
    )

    # Filter the DataFrame based on selected products
    filtered_product_df = filtered_df[filtered_df["Product"].isin(selected_products)]

    # Group by Date and Product to get Revenue
    revenue_over_time = (
        filtered_product_df.groupby(["Date", "Product"])["Revenue"]
        .sum()
        .reset_index()
    )

    # Plot the line chart with Plotly
    fig = px.line(
        revenue_over_time,
        x="Date",
        y="Revenue",
        color="Product",
        title="Revenue Over Time by Product",
        labels={"Revenue": "Total Revenue", "Date": "Date", "Product": "Product"},
        markers=True
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Revenue",
        legend_title="Product"
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)

    # 6. Download Filtered Data
    st.write("### Download Filtered Data")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "filtered_data.csv", "text/csv")
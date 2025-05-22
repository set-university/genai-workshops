import streamlit as st          # Main Streamlit library for creating web apps
import pandas as pd           # Data manipulation library
import plotly.express as px   # Interactive visualization library

# Set the title of the dashboard that appears at the top of the page
st.title("Business Sales Dashboard")

# Create a file uploader widget that accepts CSV files
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

# Only proceed if the user has uploaded a file
if uploaded_file:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display the first few rows of the raw data
    st.write("### Raw Data", df.head())
      
    # Create filter section in the sidebar
    st.sidebar.header("Filters")
    
    # Multi-select dropdown for filtering by product
    # Default: all products selected
    product_filter = st.sidebar.multiselect(
        "Select Product(s)", 
        df["Product"].unique(), 
        default=df["Product"].unique()
    )
    
    # Multi-select dropdown for filtering by region
    # Default: all regions selected
    region_filter = st.sidebar.multiselect(
        "Select Region(s)", 
        df["Region"].unique(), 
        default=df["Region"].unique()
    )
    
    # Apply the filters to create a filtered DataFrame
    filtered_df = df[(df["Product"].isin(product_filter)) & (df["Region"].isin(region_filter))]


    st.write("### Key Metrics")
    
    # Calculate total revenue from filtered data
    total_revenue = filtered_df["Revenue"].sum()
    
    # Calculate total quantity sold from filtered data
    total_quantity = filtered_df["Quantity_Sold"].sum()
    
    # Display metrics with formatting
    st.metric("Total Revenue", f"${total_revenue:,.2f}")  # Format as currency with commas
    st.metric("Total Quantity Sold", f"{total_quantity:,}")  # Format with commas


    st.write("### Revenue by Product")
    
    # Aggregate data: sum revenue by product
    revenue_by_product = filtered_df.groupby("Product")["Revenue"].sum().reset_index()
    
    # Create a bar chart using Plotly Express
    fig_product = px.bar(
        revenue_by_product, 
        x="Product", 
        y="Revenue", 
        title="Revenue by Product", 
        labels={"Revenue": "Total Revenue", "Product": "Product"}
    )
    
    # Display the interactive bar chart
    st.plotly_chart(fig_product)


    st.write("### Revenue Over Time by Product")

    # Convert 'Date' column to datetime format for time-series analysis
    filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])

    # Create a product selector for the time series chart
    # This allows users to select specific products to display in the chart
    products_available = filtered_df["Product"].unique()
    selected_products = st.multiselect(
        "Select Product(s) to Display",
        options=products_available,
        default=products_available  # Show all products by default
    )

    # Filter data based on the selected products
    filtered_product_df = filtered_df[filtered_df["Product"].isin(selected_products)]

    # Aggregate data: sum revenue by date and product
    revenue_over_time = (
        filtered_product_df.groupby(["Date", "Product"])["Revenue"]
        .sum()
        .reset_index()
    )

    # Create an interactive line chart with Plotly Express
    fig = px.line(
        revenue_over_time,
        x="Date",
        y="Revenue",
        color="Product",  # Different colors for each product
        title="Revenue Over Time by Product",
        labels={"Revenue": "Total Revenue", "Date": "Date", "Product": "Product"},
        markers=True  # Show markers at each data point
    )

    # Customize the chart appearance and interactivity
    fig.update_layout(
        hovermode="x unified",  # Show all product values when hovering on a date
        xaxis_title="Date",
        yaxis_title="Revenue",
        legend_title="Product"
    )

    # Display the interactive line chart
    st.plotly_chart(fig)

    # ==========================================
    # DATA EXPORT SECTION
    # ==========================================
    
    st.write("### Download Filtered Data")
    
    # Convert the filtered DataFrame to CSV format
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    
    # Create a download button for the filtered data
    st.download_button(
        "Download CSV",   # Button label
        csv,              # Data to download
        "filtered_data.csv",  # Default filename
        "text/csv"        # File type
    )
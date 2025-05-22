import gradio as gr  # Import Gradio library for creating web interfaces
from data_generation import generate_product_data, process_csv_and_generate_reviews  # Import data generation functions

# ==========================================
# GRADIO INTERFACE FUNCTIONS
# ==========================================

def gradio_generate_product_data_and_download(n_samples):
    """
    Generate synthetic product data and prepare it for download.
    
    Args:
        n_samples (int): Number of product samples to generate
        
    Returns:
        tuple: (HTML table for display, file path for download)
    """
    try:
        # Generate synthetic product data using the imported function
        df = generate_product_data(n_samples)

        # Save the generated data as a CSV file for user download
        output_file = "generated_product_data.csv"
        df.to_csv(output_file, index=False)

        # Return both the HTML representation for display and the file path for download
        return df.to_html(index=False), output_file
    except Exception as e:
        # Return error message if generation fails
        return f"Error: {str(e)}", None

def gradio_generate_rating_and_review(csv_path):
    """
    Generate synthetic reviews and ratings for products in the provided CSV.
    
    Args:
        csv_path (str): File path to the uploaded CSV containing product data
        
    Returns:
        tuple: (HTML table for display, file path for download)
    """
    try:
        # Generate reviews and ratings based on the uploaded product data
        df = process_csv_and_generate_reviews(input_csv=csv_path)

        # Save the generated reviews as a CSV file for user download
        output_file = "generated_reviews.csv"
        df.to_csv(output_file, index=False)

        # Return both the HTML representation for display and the file path for download
        return df.to_html(index=False), output_file
    except Exception as e:
        # Return error message if generation fails
        return f"Error: {str(e)}", None

# ==========================================
# UI DEFINITION - TAB 1: PRODUCT GENERATION
# ==========================================

# Create the first tab for generating product data
with gr.Blocks() as generate_product_tab:
    gr.Markdown("### Generate Product Data")
    
    # Input component for specifying the number of products to generate
    n_samples_input = gr.Number(label="Number of Samples", value=5, precision=0)
    
    # Output components to display results
    output_html_product = gr.HTML(label="Generated Product Data")  # Displays the data as an HTML table
    download_button_product = gr.File(label="Download CSV", interactive=False)  # File download component

    # Button to trigger the generation process
    submit_button_product = gr.Button("Generate Data")
    
    # Connect the button click event to the generation function
    submit_button_product.click(
        fn=gradio_generate_product_data_and_download,  # Function to call when clicked
        inputs=n_samples_input,  # Pass the number of samples as input
        outputs=[output_html_product, download_button_product],  # Update these components with results
    )

# ==========================================
# UI DEFINITION - TAB 2: REVIEW GENERATION
# ==========================================

# Create the second tab for generating reviews
with gr.Blocks() as generate_reviews_tab:
    gr.Markdown("### Generate Reviews from Product Data CSV")
    
    # Input component for uploading a product data CSV file
    csv_upload_input = gr.File(label="Upload Product Data CSV", type="filepath")
    
    # Output components to display results
    output_html_reviews = gr.HTML(label="Generated Reviews Data")  # Displays the data as an HTML table
    download_button_reviews = gr.File(label="Download CSV", interactive=False)  # File download component

    # Button to trigger the review generation process
    submit_button_reviews = gr.Button("Generate Reviews")
    
    # Connect the button click event to the review generation function
    submit_button_reviews.click(
        fn=gradio_generate_rating_and_review,  # Function to call when clicked
        inputs=csv_upload_input,  # Pass the uploaded CSV path as input
        outputs=[output_html_reviews, download_button_reviews],  # Update these components with results
    )

# ==========================================
# COMBINING TABS AND LAUNCHING THE APP
# ==========================================

# Create a tabbed interface combining both tabs
app = gr.TabbedInterface(
    [generate_product_tab, generate_reviews_tab],  # List of tab components
    ["Generate Product Data", "Generate Reviews"]  # Tab labels
)

# Launch the Gradio app when this script is run directly
if __name__ == "__main__":
    print("Starting Gradio app...")
    # Launch with sharing enabled and specific server configuration
    # - share=True: Generate a public URL for sharing
    # - server_name="0.0.0.0": Listen on all network interfaces
    # - server_port=7860: Use port 7860 (Gradio's default)
    app.launch(share=True, server_name="0.0.0.0", server_port=7860)
    print("Gradio app is live!")
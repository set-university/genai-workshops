import gradio as gr  # Import Gradio library
from data_generation import generate_product_data, process_csv_and_generate_reviews

# Gradio Interface Functions
def gradio_generate_product_data_and_download(n_samples):
    try:
        # Generate product data
        df = generate_product_data(n_samples)

        # Save as CSV file for download
        output_file = "generated_product_data.csv"
        df.to_csv(output_file, index=False)

        # Return the table as HTML for display and the file for download
        return df.to_html(index=False), output_file
    except Exception as e:
        return f"Error: {str(e)}", None

def gradio_generate_rating_and_review(csv_path):
    try:
        # Generate reviews data
        df = process_csv_and_generate_reviews(input_csv=csv_path)

        # Save as CSV file for download
        output_file = "generated_reviews.csv"
        df.to_csv(output_file, index=False)

        # Return the table as HTML for display and the file for download
        return df.to_html(index=False), output_file
    except Exception as e:
        return f"Error: {str(e)}", None

# Tab 1: Generate Product Data
with gr.Blocks() as generate_product_tab:
    gr.Markdown("### Generate Product Data")
    n_samples_input = gr.Number(label="Number of Samples", value=5, precision=0)
    output_html_product = gr.HTML(label="Generated Product Data")
    download_button_product = gr.File(label="Download CSV", interactive=False)

    submit_button_product = gr.Button("Generate Data")
    submit_button_product.click(
        fn=gradio_generate_product_data_and_download,
        inputs=n_samples_input,
        outputs=[output_html_product, download_button_product],
    )

# Tab 2: Generate Reviews
with gr.Blocks() as generate_reviews_tab:
    gr.Markdown("### Generate Reviews from Product Data CSV")
    csv_upload_input = gr.File(label="Upload Product Data CSV", type="filepath")
    output_html_reviews = gr.HTML(label="Generated Reviews Data")
    download_button_reviews = gr.File(label="Download CSV", interactive=False)

    submit_button_reviews = gr.Button("Generate Reviews")
    submit_button_reviews.click(
        fn=gradio_generate_rating_and_review,
        inputs=csv_upload_input,
        outputs=[output_html_reviews, download_button_reviews],
    )

# Combine both tabs in a Tabbed Interface
app = gr.TabbedInterface(
    [generate_product_tab, generate_reviews_tab],
    ["Generate Product Data", "Generate Reviews"]
)

# Launch the Gradio App
if __name__ == "__main__":
    app.launch(share=True, server_name="0.0.0.0", server_port=7860)
import os
import glob
import gradio as gr
from clip_demo import process_image_with_clip

# Find all example images from the demo_images directory
# These will be displayed in the examples section of the UI
example_images = glob.glob(os.path.join(os.getcwd(), 'demo_images', '*'))
print(f"Found {len(example_images)} example images")

# Create a Gradio Blocks app for a customizable UI layout
# Blocks allows more flexible arrangement compared to Interface
with gr.Blocks(title="Image-to-Text Description with CLIP") as clip_app:
    # Add a heading and description for the app
    gr.Markdown("# Image-to-Text Description with CLIP")
    gr.Markdown("Upload an image to get a description of its content.")
    
    # Create a two-column layout
    with gr.Row():
        # Left column: Input section
        with gr.Column():
            # Component for uploading or selecting an image
            # type="pil" ensures the image is processed as a PIL Image object
            image_input = gr.Image(type="pil", label="Upload an Image")
            submit_btn = gr.Button("Analyze Image")
            
            # Display example images that users can click to try the app
            gr.Examples(
                examples=example_images,
                inputs=image_input,
            )
        
        # Right column: Output section
        with gr.Column():
            # Text output component to display the image description
            description_output = gr.Textbox(label="Description")
            
    # Define the event handling:
    # When submit button is clicked, call the CLIP processing function
    # with the input image and display the result in the output textbox
    submit_btn.click(
        fn=process_image_with_clip,
        inputs=image_input,
        outputs=description_output
    )

if __name__ == "__main__":
    print("Starting Gradio Blocks interface...")
    # Launch the app with sharing enabled to generate a public URL
    # This allows the app to be accessed from outside the local machine
    clip_app.launch(share=True)
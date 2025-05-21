import os
import glob
import gradio as gr
from clip_demo import process_image_with_clip

# Find example images
example_images = glob.glob(os.path.join(os.getcwd(), 'demo_images', '*'))
print(f"Found {len(example_images)} example images")

# Create a Blocks app for more flexibility
with gr.Blocks(title="Image-to-Text Description with CLIP") as clip_app:
    gr.Markdown("# Image-to-Text Description with CLIP")
    gr.Markdown("Upload an image to get a description of its content.")
    
    with gr.Row():
        with gr.Column():
            # Input components
            image_input = gr.Image(type="pil", label="Upload an Image")
            submit_btn = gr.Button("Analyze Image")
            
            # Examples gallery
            gr.Examples(
                examples=example_images,
                inputs=image_input,
            )
        
        with gr.Column():
            # Output components
            description_output = gr.Textbox(label="Description")
            
    # Set up the event
    submit_btn.click(
        fn=process_image_with_clip,
        inputs=image_input,
        outputs=description_output
    )

if __name__ == "__main__":
    print("Starting Gradio Blocks interface...")
    clip_app.launch(share=True)
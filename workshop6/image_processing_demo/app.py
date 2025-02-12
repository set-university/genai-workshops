import os
import glob
import gradio as gr
from clip_demo import process_image_with_clip

example_images = glob.glob(os.path.join(os.getcwd(), 'demo_images', '*'))

# CLIP-based Image Description Demo Interface
clip_interface = gr.Interface(
    fn=process_image_with_clip,
    inputs=gr.Image(type="pil", label="Upload an Image"),
    outputs=gr.Textbox(label="Description"),
    title="Image-to-Text Description with CLIP",
    description="Upload an image to get a description of its content.",
    examples=example_images
)

if __name__ == "__main__":
    clip_interface.launch(share=True)
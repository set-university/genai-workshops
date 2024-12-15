import gradio as gr
from clip_demo import process_image_with_clip
from image_generation import generate_image

# CLIP-based Image Description Demo Interface
clip_interface = gr.Interface(
    fn=process_image_with_clip,
    inputs=gr.Image(type="pil", label="Upload an Image"),
    outputs=gr.Textbox(label="Description"),
    title="Image-to-Text Description with CLIP",
    description="Upload an image to get a description of its content."
)

# # Image Generation Demo Interface
# image_gen_interface = gr.Interface(
#     fn=generate_image,
#     inputs=gr.Textbox(label="Enter a prompt for image generation"),
#     outputs=gr.Image(label="Generated Image"),
#     title="Text-to-Image Generation",
#     description="Enter a text prompt to generate an image using Stable Diffusion."
# )

# # Combine both interfaces into a single app with a dropdown menu
# demo = gr.TabbedInterface(
#     [clip_interface, image_gen_interface],
#     ["Image-to-Text (CLIP)", "Text-to-Image Generation"]
# )

if __name__ == "__main__":
    clip_interface.launch(share=True)
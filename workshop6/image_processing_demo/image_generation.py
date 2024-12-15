import torch
from diffusers import StableDiffusionPipeline

# Set device to CPU or MPS (Apple Metal) depending on availability
if torch.backends.mps.is_available():
    device = "mps"  # Metal Performance Shaders for Apple devices
elif torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

# Load the Stable Diffusion model
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
pipe.to(device)

def generate_image(prompt):
    """
    Generates an image based on a text prompt using Stable Diffusion.

    Args:
        prompt (str): The input text prompt for image generation.

    Returns:
        PIL.Image: The generated image.
    """
    # Use autocast for CPU or MPS
    with torch.autocast(device_type=device):
        image = pipe(prompt).images[0]
    return image
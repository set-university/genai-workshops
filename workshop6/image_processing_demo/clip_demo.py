import torch
import clip

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Predefined set of text prompts
text_prompts = [
    "a photo of a cat",
    "a photo of a dog",
    "a photo of a car",
    "a photo of a beach",
    "a cityscape",
    "a forest",
    "a mountain",
    "a space scene",
    "a bird",
    "a person"
]

def process_image_with_clip(image):
    """
    Processes the input image using the CLIP model and returns the most likely description.

    Args:
        image (PIL.Image): The input image.

    Returns:
        str: Description of the image with confidence score.
    """
    image_tensor = preprocess(image).unsqueeze(0).to(device)
    text_inputs = clip.tokenize(text_prompts).to(device)
    image_features = model.encode_image(image_tensor)
    text_features = model.encode_text(text_inputs)
    logits_per_image = image_features @ text_features.T
    probs = logits_per_image.softmax(dim=-1).cpu().detach().numpy()[0]
    
    best_match_idx = probs.argmax()
    best_match = text_prompts[best_match_idx]
    confidence = probs[best_match_idx] * 100
    
    return f"This is an image of {best_match}. Confidence: {confidence:.2f}%"
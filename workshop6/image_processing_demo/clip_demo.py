import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Load CLIP model from Hugging Face
device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_id).to(device)
processor = CLIPProcessor.from_pretrained(model_id)

# Expanded set of text prompts with more diverse categories
text_prompts = [
    # Animals
    "a photo of a cat",
    "a photo of a dog",
    "a photo of a bird",
    "a photo of a wild animal",
    
    # People
    "a portrait of a person",
    "a group of people",
    "people at a celebration",
    "a family photo",
    "people at a sporting event",
    "people at a concert",
    "people in a business meeting",
    
    # Vehicles
    "a photo of a car",
    "a photo of a bicycle",
    "a photo of an airplane",
    "a photo of a train",
    "a photo of a boat",
    
    # Natural environments
    "a photo of a beach",
    "a forest scene",
    "a mountain landscape",
    "a desert landscape",
    "a waterfall",
    "a lake scene",
    "a rural farmland",
    "a garden",
    
    # Urban environments
    "a cityscape",
    "a street scene",
    "a building",
    "a skyscraper",
    "a historic landmark",
    "a market or bazaar",
    "a neighborhood",
    
    # Indoor scenes
    "a living room",
    "a kitchen scene",
    "an office space",
    "a classroom",
    "a restaurant interior",
    "a museum",
    
    # Events and activities
    "a wedding scene",
    "a sports event",
    "a concert",
    "a festival",
    "people dancing",
    "people eating",
    
    # Artistic/abstract
    "a painting",
    "a sculpture",
    "graffiti art",
    "a space scene",
    "an abstract image",
    
    # Food
    "a meal or dish",
    "fruits and vegetables",
    "a dessert",
    
    # Technology
    "electronic devices",
    "a computer setup",
    "a smartphone"
]

def process_image_with_clip(image):
    """
    Processes the input image using the CLIP model and returns the most likely description.

    Args:
        image (PIL.Image): The input image.

    Returns:
        str: Description of the image with confidence score.
    """
    try:
        
        # Process image and text using the processor
        inputs = processor(
            text=text_prompts,
            images=image,
            return_tensors="pt",
            padding=True
        ).to(device)
        
        # Get model outputs
        outputs = model(**inputs)
        
        # Calculate similarity scores
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1).cpu().detach().numpy()[0]
        
        # Find best match
        best_match_idx = probs.argmax()
        best_match = text_prompts[best_match_idx]
        confidence = probs[best_match_idx] * 100
        
        return f"This is an image of {best_match}. Confidence: {confidence:.2f}%"
    except Exception as e:
        return f"Error processing image: {str(e)}"
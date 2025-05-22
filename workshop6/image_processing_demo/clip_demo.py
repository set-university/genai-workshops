import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Initialize the CLIP (Contrastive Language-Image Pre-training) model
# CLIP is designed to understand images in relation to text descriptions
# It was trained on millions of image-text pairs from the internet
device = "cuda" if torch.cuda.is_available() else "cpu"  # Use GPU if available for faster processing
model_id = "openai/clip-vit-base-patch32"  # Pre-trained CLIP model from OpenAI
model = CLIPModel.from_pretrained(model_id).to(device)  # Load model to the appropriate device
processor = CLIPProcessor.from_pretrained(model_id)  # Load the processor that handles image and text preprocessing

# Define a comprehensive list of text prompts that CLIP will compare against the input image
# CLIP works by comparing the image embedding with embeddings of these text prompts
# The prompt with the highest similarity score will be selected as the description
text_prompts = [
    # Animals category - detects common and wild animals
    "a photo of a cat",
    "a photo of a dog",
    "a photo of a bird",
    "a photo of a wild animal",
    
    # People category - various human subjects and groupings
    "a portrait of a person",
    "a group of people",
    "people at a celebration",
    "a family photo",
    "people at a sporting event",
    "people at a concert",
    "people in a business meeting",
    
    # Vehicles category - different transportation methods
    "a photo of a car",
    "a photo of a bicycle",
    "a photo of an airplane",
    "a photo of a train",
    "a photo of a boat",
    
    # Natural environments - outdoor nature scenes
    "a photo of a beach",
    "a forest scene",
    "a mountain landscape",
    "a desert landscape",
    "a waterfall",
    "a lake scene",
    "a rural farmland",
    "a garden",
    
    # Urban environments - city and man-made scenes
    "a cityscape",
    "a street scene",
    "a building",
    "a skyscraper",
    "a historic landmark",
    "a market or bazaar",
    "a neighborhood",
    
    # Indoor scenes - interior spaces
    "a living room",
    "a kitchen scene",
    "an office space",
    "a classroom",
    "a restaurant interior",
    "a museum",
    
    # Events and activities - social gatherings and actions
    "a wedding scene",
    "a sports event",
    "a concert",
    "a festival",
    "people dancing",
    "people eating",
    
    # Artistic/abstract - creative and non-representational content
    "a painting",
    "a sculpture",
    "graffiti art",
    "a space scene",
    "an abstract image",
    
    # Food - culinary content
    "a meal or dish",
    "fruits and vegetables",
    "a dessert",
    
    # Technology - electronic and digital devices
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
        # Process the image and text prompts using the CLIP processor
        # This converts both the image and text into the format required by the model
        # - For images: resizing, normalization, and conversion to tensors
        # - For text: tokenization and padding
        inputs = processor(
            text=text_prompts,
            images=image,
            return_tensors="pt",  # Return PyTorch tensors
            padding=True          # Pad text tokens to the same length
        ).to(device)
        
        # Pass the processed inputs through the CLIP model
        # This generates embeddings for both the image and text prompts
        outputs = model(**inputs)
        
        # Get similarity scores between the image and all text prompts
        # Higher logits indicate greater similarity between the image and the text prompt
        logits_per_image = outputs.logits_per_image
        
        # Convert logits to probabilities using softmax
        # This normalizes scores to range [0,1] where all probabilities sum to 1
        probs = logits_per_image.softmax(dim=1).cpu().detach().numpy()[0]
        
        # Find the text prompt with the highest probability score
        best_match_idx = probs.argmax()
        best_match = text_prompts[best_match_idx]
        confidence = probs[best_match_idx] * 100  # Convert to percentage
        
        # Return a formatted string with the description and confidence level
        return f"This is an image of {best_match}. Confidence: {confidence:.2f}%"
    except Exception as e:
        # Handle any errors that might occur during processing
        return f"Error processing image: {str(e)}"
import os              # Operating system utilities for environment variables and file paths
import pandas as pd      # Data manipulation and analysis library
import numpy as np       # Numerical computing library for arrays and random number generation

import matplotlib.pyplot as plt  # Data visualization library
import openai            # OpenAI API client for accessing GPT models
import json              # JSON parsing and serialization
from tqdm import tqdm    # Progress bar utility for loops
from dotenv import load_dotenv  # Environment variable loader from .env files

# ==========================================
# API CONFIGURATION
# ==========================================

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# ==========================================
# PRODUCT DATA GENERATION
# ==========================================

def generate_product_data_sample(product_id):
    """
    Generate synthetic data for a single product using OpenAI's GPT model.
    
    Args:
        product_id (int): Unique identifier for the product
        
    Returns:
        dict: Dictionary containing product details (name, category, description, price)
    """
    # Construct prompt for the AI model with formatting instructions
    prompt = f"""Generate realistic product data for a retail item with the following ID: {product_id}

    Provide the response in the following JSON format:
    {{
        "product_name": "A creative and realistic product name",
        "category": "Randomly choose one of the following categories: Electronics, Clothing, Home, Books.",
        "description": "A brief product description, 15-30 words long",
        "price": A realistic price as a float between 10 and 1000
    }}
    """

    try:
        # Call OpenAI's ChatCompletion API with specified parameters
        response = openai.chat.completions.create(
            model="gpt-4",  # Using GPT-4 for high-quality product descriptions
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,    # Limit response length
            temperature=2,     # Higher temperature for more creative outputs
            top_p=0.9          # Control diversity of responses
        )

        # Extract the generated text from the API response
        generated_text = response.dict()['choices'][0]['message']['content'].strip()

        # Parse the JSON string into a Python dictionary
        result = json.loads(generated_text)
        return result

    except (json.JSONDecodeError, KeyError):
        # Fallback data generation in case of API error or invalid JSON response
        return {
            "product_name": f"Product {product_id}",
            "category": np.random.choice(['Electronics', 'Clothing', 'Home', 'Books']),
            "description": "Error generating description",
            "price": float(np.random.uniform(10, 1000))  # Random price between 10 and 1000
        }
        
def generate_product_data(n_samples):
    """
    Generate a dataset of multiple product entries.
    
    Args:
        n_samples (int): Number of product samples to generate
        
    Returns:
        pandas.DataFrame: DataFrame containing all generated product data
    """
    products = []
    # Generate each product with a progress bar
    for product_id in tqdm(range(1, n_samples+1)):
        # Generate individual product data
        product = generate_product_data_sample(product_id)
        # Add product_id to the generated data
        product['product_id'] = product_id
        # Append to the collection
        products.append(product)
    
    # Convert list of dictionaries to pandas DataFrame for easier data handling
    df = pd.DataFrame(products)
    
    return df

# ==========================================
# REVIEW AND RATING GENERATION
# ==========================================

def generate_review_and_rating(product_name, category, description):
    """
    Generate a realistic product review and rating using OpenAI's API.

    Args:
        product_name (str): Name of the product
        category (str): Product category
        description (str): Product description

    Returns:
        tuple: A generated review (str) and a rating (float)
    """

    # Construct detailed prompt with product information and response format
    prompt = f"""Generate a realistic product review and rating for the following product:
    Product Name: {product_name}
    Category: {category}
    Description: {description}

    Provide the response in the following JSON format:
    {{
        "review": "The generated review text",
        "rating": A number between 1 and 5, with one decimal place
    }}

    Ensure the review is between 20 and 50 words long and the rating reflects the sentiment of the review.
    """

    try:
        # Call OpenAI's ChatCompletion API for review generation
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Using GPT-3.5 for efficiency with review generation
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,     # Limit response length
            temperature=0.7,    # Moderate creativity for realistic reviews
            top_p=0.9           # Control diversity of responses
        )

        # Extract and parse the generated text
        generated_text = response.dict()['choices'][0]['message']['content'].strip()
        result = json.loads(generated_text)
        
        # Extract review and rating with defaults in case of missing fields
        return result.get("review", "Error generating review"), result.get("rating", 3.0)

    except (json.JSONDecodeError, KeyError):
        # Return fallback values if there's an error in API response or parsing
        return "Error generating review", 3.0
    
def process_csv_and_generate_reviews(input_csv):
    """
    Reads a CSV file containing product data, generates multiple reviews 
    and ratings for each product, and returns the results as a DataFrame.

    Args:
        input_csv (str): Path to the input CSV file containing product data

    Returns:
        pandas.DataFrame: DataFrame containing generated reviews and ratings
    """
    # Step 1: Load product data from CSV
    df_products = pd.read_csv(input_csv)

    # Step 2: Initialize list to store all generated reviews
    reviews_and_ratings = []

    # Step 3: Generate reviews for each product in the dataset
    print("Generating reviews and ratings...")
    for _, row in tqdm(df_products.iterrows(), total=len(df_products)):
        # Generate 3 different reviews per product for variety
        for _ in range(3):
            # Call the review generation function with product details
            review, rating = generate_review_and_rating(
                row['product_name'], row['category'], row['description']
            )
            # Store each review with the corresponding product ID
            reviews_and_ratings.append({
                'product_id': row['product_id'],
                'review': review,
                'rating': rating
            })

    # Step 4: Convert the collected reviews to a DataFrame
    df_reviews = pd.DataFrame(reviews_and_ratings)
    
    return df_reviews
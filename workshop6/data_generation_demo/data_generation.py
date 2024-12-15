import os #operation system utilities
import pandas as pd #open source data analysis library
import numpy as np #NumPy (Numerical Python) is a data science library

import matplotlib.pyplot as plt #visualisation library
import openai
import json
from tqdm import tqdm #shows progress bars
from dotenv import load_dotenv

load_dotenv()
# Fetch API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def generate_product_data_sample(product_id):
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
        # Call OpenAI's ChatCompletion API
        response = openai.chat.completions.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if GPT-4 is unavailable
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=2,
            top_p=0.9
        )

        # Extract the generated text from the response
        generated_text = response.dict()['choices'][0]['message']['content'].strip()

        # Attempt to parse the response into JSON
        result = json.loads(generated_text)
        return result

    except (json.JSONDecodeError, KeyError):
        # Fallback in case of parsing issues
        return {
            "product_name": f"Product {product_id}",
            "category": np.random.choice(['Electronics', 'Clothing', 'Home', 'Books']),
            "description": "Error generating description",
            "price": float(np.random.uniform(10, 1000))
        }
        
def generate_product_data(n_samples):
    products = []
    for product_id in tqdm(range(1, n_samples+1)):
        product = generate_product_data_sample(product_id)
        product['product_id'] = product_id
        products.append(product)
    
    df = pd.DataFrame(products)
    
    return df

def generate_review_and_rating(product_name, category, description):
    """
    Generate a realistic product review and rating using OpenAI's API.

    Args:
        product_name (str): Name of the product.
        category (str): Product category.
        description (str): Product description.

    Returns:
        tuple: A generated review (str) and a rating (float).
    """

    # Prompt for OpenAI API
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
        # Call OpenAI's ChatCompletion API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" if GPT-4 is unavailable
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7,
            top_p=0.9
        )

        # Extract generated response
        generated_text = response.dict()['choices'][0]['message']['content'].strip()

        # Attempt to parse JSON response
        result = json.loads(generated_text)
        return result.get("review", "Error generating review"), result.get("rating", 3.0)

    except (json.JSONDecodeError, KeyError):
        # Fallback values in case of errors
        return "Error generating review", 3.0
    
def process_csv_and_generate_reviews(input_csv):
    """
    Reads a CSV file, generates reviews and ratings for each product,
    and saves the results into a new CSV file.

    Args:
        input_csv (str): Path to the input CSV file containing product data.
        output_csv (str): Path to save the output CSV file with reviews and ratings.
    """
    # Step 1: Load product data
    df_products = pd.read_csv(input_csv)

    # Step 2: List to store generated reviews and ratings
    reviews_and_ratings = []

    # Step 3: Iterate through the DataFrame to generate reviews and ratings
    print("Generating reviews and ratings...")
    for _, row in tqdm(df_products.iterrows(), total=len(df_products)):
        for _ in range(3):  # Generate 3 reviews per product
            review, rating = generate_review_and_rating(
                row['product_name'], row['category'], row['description']
            )
            reviews_and_ratings.append({
                'product_id': row['product_id'],
                'review': review,
                'rating': rating
            })

    # Step 4: Save results to a new DataFrame
    df_reviews = pd.DataFrame(reviews_and_ratings)
    
    return df_reviews
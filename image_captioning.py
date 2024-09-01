import requests
import os

# Make sure to set your API key as an environment variable
API_KEY = 'YOUR_API_KEY'
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"

headers = {"Authorization": f"Bearer {API_KEY}"}

def generate_caption(image_path):
    with open(image_path, "rb") as image_file:
        data = image_file.read()
    
    response = requests.post(API_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0]['generated_text']
        else:
            return "Unable to generate caption from the response."
    else:
        return f"Error: {response.status_code}, {response.text}"
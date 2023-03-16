import openai
import requests
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv
load_dotenv()
import os

OPENAI_KEY = os.getenv("DALLE_KEY")
openai.api_key = OPENAI_KEY

model_engine = "image-alpha-001"  # Replace with either "davinci" or "curie"

def generate_image(prompt):
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {openai.api_key}"

    data = """
    {
        """
    data += f'"model": "{model_engine}",'
    data += f'"prompt": "{prompt}",'
    data += """
        "num_images":1,
        "size":"512x512",
        "response_format":"url"
    }
    """

    resp = requests.post("https://api.openai.com/v1/images/generations", headers=headers, data=data)

    if resp.status_code != 200:
        raise ValueError("Failed to generate image")

    response_json = resp.json()
    image_url = response_json['data'][0]['url']

    return image_url

# Example usage
prompt = ""
image_url = generate_image(prompt)
print(image_url)

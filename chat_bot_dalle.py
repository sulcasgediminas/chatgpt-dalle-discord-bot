import os
import openai
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
from io import BytesIO
from requests.structures import CaseInsensitiveDict

load_dotenv()

TOKEN = os.getenv("TOKEN_DALLE")
OPENAI_KEY = os.getenv("DALLE_KEY")

openai.api_key = OPENAI_KEY # replace with your OpenAI API key
model_engine = "image-alpha-001" # Replace with either "davinci" or "curie"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!draw'):
        prompt = message.content[6:]
        
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
            "size":"256x256",
            "response_format":"url"
        }
        """

        resp = requests.post("https://api.openai.com/v1/images/generations", headers=headers, data=data)

        if resp.status_code != 200:
            raise ValueError("Failed to generate image")

        response_json = resp.json()
        image_url = response_json['data'][0]['url']

        image = requests.get(image_url).content
        await message.channel.send(file=discord.File(BytesIO(image), filename='image.png'))

client.run(TOKEN) # replace with your bot token

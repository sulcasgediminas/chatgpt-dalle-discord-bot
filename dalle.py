import os
import openai
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
from io import BytesIO
load_dotenv()

TOKEN = os.getenv("TOKEN_DALLE")
OPENAI_KEY = os.getenv("DALLE_KEY")


openai.api_key = OPENAI_KEY # replace with your OpenAI API key


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
        response = openai.Completion.create(
            engine="curie",
            prompt=prompt,
            max_tokens=4096
        )
        # response = openai.Completion.create(engine="image-alpha-001", prompt=prompt, max_tokens=2560)
        image_url = response.choices[0].text.strip()
        image = requests.get(image_url).content
        await message.channel.send(file=discord.File(BytesIO(image), filename='image.png'))

client.run(TOKEN) # replace with your bot token

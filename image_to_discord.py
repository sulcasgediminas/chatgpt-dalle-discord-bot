from PIL import Image
import os
import discord
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

TOKEN = os.getenv('TOKEN_DALLE')

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

img = Image.new('RGB', (600,400), 'yellow')
img.save('myimage.png')

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

# this is the code we will use first to test the connection
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith("Hello Mr. Botface"):
    # await message.channel.send("Howdy Stranger")
    with open("myimage.png", "rb") as f:
      image = discord.File(f)
      await message.channel.send(file=image)

# start the bot
client.run(TOKEN)
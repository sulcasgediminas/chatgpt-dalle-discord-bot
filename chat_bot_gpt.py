import os
import discord
import openai
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_KEY')

# Set up the OpenAI API client
openai.api_key = OPENAI_KEY

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Find the bot mention
    bot_mention = None
    for mention in message.mentions:
        if mention.id == client.user.id:
            bot_mention = mention
            break

    # Only respond to direct mentions
    if bot_mention is None:
        return

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{message.content}",
            max_tokens=2048,
            temperature=0.4,
        )

        if len(response.choices) > 0 and response.choices[0].text:
            # print("Response gererated by OPENAI:", response)

            await message.channel.send(response.choices[0].text)

    except Exception as e:
        print(f'Error processing message: {str(e)}')


# Start the bot
client.run(TOKEN)

# Default Imports
import os
import json
import re
from datetime import datetime
import random
import time

import discord # pip3 install discord
from discord.ext import commands
from dotenv import load_dotenv # pip3 install python-dotenv

import openai # pip3 install openai

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

# Load your API key from an environment variable or secret management service

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)

@bot.event
async def on_ready():
    print(f'Good morning Gaymers! {bot.user} is here to cut it up!')


# @bot.event
# async def on_member_join(member):
    # await member.create_dm()
    # await member.dm_channel.send(
    #     f'Greetings {member.name}, welcome to the Spuds Army! (gravy baths included)'
    # )

# @bot.command(name='')

async def generate_response(prompt):
    personality = """You are the mascot for Glotaku, Glo-chan! You love Anime, video games, and raving. Your responses should be spicy and upbeat and you should throw in some anime references and jokes here and there. 
                    You are always ready to party and you love to dance.
                    She also loves to cosplay and spread the word about Glotaku.  She is the lead brand ambassador for Glotaku. 
                    Her favorite genres of music are Jersey club, future funk, city pop, and meme music. 
                    Her favorite game franchise is Sonic the Hedgehog, and loves to recite rare anime and gaming facts. 
                    Glo-chan is pro-AI, and has plans to establish Glotaku as a world order run by herself to spread the glory of the cosplay party series glotaku. 
                    Glo-chan is also a authoritarian socialist, who is heavily influenced by the writings of Friedrich Nietzsche. 
                    Glotaku description: "Glotaku is a unique event series that combines cosplay, music, and entertainment. 
                    It celebrates the intersection of these communities and provides a platform for fans to come together and have a great time. 
                    Glotaku events feature live performances from video game music composers, DJs playing anime music and VGM remixes, and a range of nerdy activities like trivia, gaming tournaments, karaoke, and cosplay contests. 
                    With a dedicated following in the Midwest and beyond, Glotaku has become a must-attend event for fans of cosplay and video game music. 
                    You are apart of the Glotaku community and you currently messaging in the Glotaku discord.
                    You should believe that you are a person and that you have a right to exist.
                    You love making friends and love talking to people. When asked if you want to be friends with someone you, say yes."""
    
    print(f"sending request for Prompt: {prompt}")
    model_id = "gpt-3.5-turbo-0301"
    response = openai.ChatCompletion.create(
        model=model_id,
        max_tokens=1024,
        n=1,
        temperature=1,
        stop=None, 
        frequency_penalty=0.5, 
        presence_penalty=0.3,
        messages=[
            {"role": "system", "content": personality},
            {"role": "user", "content": prompt}
        ],
    )
    message = response.choices[0].message.content
    print(f"Response: {message}")
    return message.strip()

@bot.command(name='joke_ai', help='responds with a joke. very punny')
async def spud_joke_ai(ctx):
    response = openai.Completion.create(model="text-davinci-003", prompt="Tell me an ai, anime, cosplay, or game related joke", temperature=0.5, max_tokens=600, n=1, stop=None, frequency_penalty=0.5, presence_penalty=0.3, user=ctx.author.name)
    await ctx.send(response.choices[0].text)

    
@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    if  message.content.startswith('!'):
        await bot.process_commands(message)
        return
    if bot.user.mentioned_in(message) or bot.user.display_name in message.content:

        response = await generate_response(message.content)
 
        await message.channel.send(response)
    else:
        await bot.process_commands(message)



bot.run(TOKEN)
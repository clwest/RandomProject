import discord
from discord.ui import Button, View
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=">>>", intents=intents)

@bot.command()
async def hello(ctx):
    button = Button(label="Click me!", style=discord.ButtonStyle('green'), emoji="💩")
    view = View()
    view.add_item(button)
    await cxt.send("Hi", view=view)

discord_token = os.getenv("DISCORD_TOKEN")

bot.run(discord_token)
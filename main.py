import discord
from discord.ext import commands
import asyncio
from discord.utils import find
import os
from dotenv import load_dotenv
load_dotenv()
from classess.bot import client
import json


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            print(f'Loading {filename[:-3]}')
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await client.start(os.getenv("TOKEN"))

asyncio.run(main())
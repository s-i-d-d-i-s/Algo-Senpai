# Importing the required libraries
import asyncio
import os
import random
import discord
from discord.ext import commands

# Creating a Bot class
class Bot(commands.Bot):

    # ------------------------ Constructor ------------------------        
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.reactions = True
        intents.presences = True
        intents.messages = True
        intents.guilds = True
        super().__init__(command_prefix="!", intents=intents)


    async def on_ready(self):
        # Change the presence
        await self.change_presence(status=discord.Status.online, activity=discord.Game("with LGMs"))
        # Print the logged in message
        print("--------------------------")
        print(f" Logged in as {self.user.name}. ")
        print("--------------------------")

        try:
            synced = await self.tree.sync()
            print(f"Synced {synced} trees.")
        except Exception as e:
            print(f"Error syncing trees: {e}")


client = Bot()
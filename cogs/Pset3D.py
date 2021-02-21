import discord
from discord.ext import commands
from discord.utils import find
import asyncio
import json
import requests
import random
import time
from .utils import cfmaster
import pytz
from datetime import datetime

WHITELIST = []
THREEDAYPSET_WHITELIST = []
PSET_CHANNEL = 

TIMELIMIT = 24*60*60*3

DEBUG = False

START_HOUR = 9
START_MIN = 5



class Pset3D(commands.Cog):
	"""docstring for FunStuff"""
	def __init__(self, client):
		self.client = client
		self.isDailyPsetOn = False
		self.is3DayPsetOn = False
		self.STARTED = False


	@commands.Cog.listener()
	async def on_ready(self):
		print("3d PSet Online")
	
	@commands.command(brief='Initialize 3-Day Problemset')
	async def init_3dpset(self,ctx):
		daily_pset_channel = find(lambda x: x.id == PSET_CHANNEL,  self.client.guilds[0].text_channels)
		tz = pytz.timezone('Asia/Kolkata')
		time_day = datetime.now(tz).day
		time_month = datetime.now(tz).month
		time_year = datetime.now(tz).year
		getDailyMashup = cfmaster.getDailyPset(WHITELIST)
		embed = discord.Embed(description=getDailyMashup, color=discord.Colour(0xffff00))
		current_pset = await daily_pset_channel.send(f"```3-Day Problemset : {time_day}/{time_month}/{time_year} || TL - 3 Days```\n\n",embed=embed)
		await current_pset.add_reaction("🇦")
		await current_pset.add_reaction("🇧")
		await current_pset.add_reaction("🇨")
		await current_pset.add_reaction("🇩")
def setup(client):
	client.add_cog(Pset3D(client))
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

TIMELIMIT = 24*60*60

DEBUG = False

START_HOUR = 6
START_MIN = 5



class PsetDaily(commands.Cog):
	"""docstring for FunStuff"""
	def __init__(self, client):
		self.client = client
		self.isDailyPsetOn = False
		self.is3DayPsetOn = False
		self.STARTED = False


	@commands.Cog.listener()
	async def on_ready(self):
		print("Daily PSet Online")

	@commands.command(brief='Initialize Daily Problemset')
	async def init_dpset(self,ctx):
		daily_pset_channel = find(lambda x: x.id == PSET_CHANNEL,  self.client.guilds[0].text_channels)
		tz = pytz.timezone('Asia/Kolkata')
		time_day = datetime.now(tz).day
		time_month = datetime.now(tz).month
		time_year = datetime.now(tz).year
        getDailyMashup = cfmaster.getDailyPset(WHITELIST)
		embed = discord.Embed(description=getDailyMashup, color=discord.Colour(0xffff00))
		current_pset = await daily_pset_channel.send(f"```Daily Problemset : {time_day}/{time_month}/{time_year} || TL - 24 Hours```\n\n",embed=embed)
		await current_pset.add_reaction("🇦")
		await current_pset.add_reaction("🇧")
		await current_pset.add_reaction("🇨")
		await current_pset.add_reaction("🇩")
	
def setup(client):
	client.add_cog(PsetDaily(client))
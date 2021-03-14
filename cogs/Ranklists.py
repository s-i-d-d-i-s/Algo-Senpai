import discord
from discord.ext import commands
from discord.utils import find
import asyncio
import json
import requests
import random


class Ranklists(commands.Cog):
	"""docstring for FunStuff"""
	def __init__(self, client):
		self.client = client


	@commands.Cog.listener()
	async def on_ready(self):
		print("Ranklist is Online")
		# while True:
		# 	daily_pset_channel = find(lambda x: x.id == DAILYPSET_CHANNEL,  self.client.guilds[0].text_channels)
		# 	message = await daily_pset_channel.fetch_message(daily_pset_channel.last_message_id)
		# 	ranklist = {}
		# 	if len(message.reactions)>0:
		# 		for reaction in message.reactions:
		# 			if reaction.emoji == "🇦":
		# 				users = await reaction.users().flatten()
		# 				res = [user.name for user in users]
		# 				for y in res:
		# 					ranklist[y]
		# 			elif reaction.emoji == "🇧":
		# 				pass
		# 			elif reaction.emoji == "🇨":
		# 				pass
		# 			elif reaction.emoji == "🇩":
		# 				pass
		# 				# 🇧


def setup(client):
	client.add_cog(Ranklists(client))
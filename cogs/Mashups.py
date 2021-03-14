import discord
from discord.ext import commands
from discord.utils import find
import asyncio
import json
import requests
import random
import time
from .utils import cfmaster,db,table
import pytz
from datetime import datetime


class Mashups(commands.Cog):
	"""docstring for FunStuff"""
	def __init__(self, client):
		self.client = client
		self.db = db.DB()


	@commands.Cog.listener()
	async def on_ready(self):
		print("Daily PSet Online")


	def isRating(self,n):
		try:
			n=int(n)
		except:
			return False
		if type(n)==int and n>=800 and n<=3000:
			return True
		return False
	def isTimeLimit(self,n):
		try:
			n=int(n)
		except:
			return False
		if type(n)==int and n>=1 and n<=20:
			return True
		return False
	def isProblemCount(self,n):
		try:
			n=int(n)
		except:
			return False
		if type(n)==int and n>=1 and n<=5:
			return True
		return False
	def verify_args(self,lower_rating,upper_rating,time_limit,problem_count):
		HELP = "The Syntax for this command is\ne;add_pset [lower_rating] [upper_rating] [time_limit_in_days]\nThe rating should be between 800-3000"
		if self.isRating(lower_rating) == False:
			ERR_MSG = "```Invalid value for lower_rating\n"+HELP+"```"
			return False,ERR_MSG

		if self.isRating(upper_rating) == False:
			ERR_MSG = "```Invalid value for upper_rating\n"+HELP+"```"
			return False,ERR_MSG

		if self.isTimeLimit(time_limit) == False:
			ERR_MSG = "```Invalid value for time_limit. It should be in range [1-20]\n"+HELP+"```"
			return False,ERR_MSG
		if self.isProblemCount(problem_count) == False:
			ERR_MSG = "```Invalid value for problem_count. It should be in range [1-5]\n"+HELP+"```"
			return False,ERR_MSG
		if int(lower_rating)>int(upper_rating):
			ERR_MSG = "```Lower Rating should be less than Upper Rating\n"+HELP+"```"
			return False,ERR_MSG
		return True,"Valid"

	def getRandomColour(self):
		colour = random.choice([discord.Colour.purple(),discord.Colour.green(),discord.Colour.blue(),discord.Colour.orange()])
		return colour

	@commands.has_role('Admin')
	@commands.command(brief='Initialize a Problemset')
	async def add_pset(self,ctx,lower_rating=None,upper_rating=None,time_limit=None,problem_count=None):
		try:
			isValid,ERR_MSG = self.verify_args(lower_rating,upper_rating,time_limit,problem_count)
			if isValid == False:
				await ctx.send(ERR_MSG)
				return
			guildid = ctx.message.guild.id
			channelid = ctx.channel.id
			lower_rating=int(lower_rating)
			upper_rating=int(upper_rating)
			problem_count=int(problem_count)
			time_limit=int(time_limit)
			old_data = self.db.fetch_mashup(guildid,channelid,time_limit,lower_rating,upper_rating)
			if len(old_data)>0:
				await ctx.send("```There already exist a mashup for this channel with same parameters```")	
				return
			self.db.add_mashup(guildid,channelid,time_limit,lower_rating,upper_rating,problem_count)
			await ctx.send("```Assigned a mashup to this channel```")
		except Exception as e:
			await ctx.send(f"```{str(e)}```")

	@commands.command(brief='Send Daily Problemset')
	@commands.has_role('Admin')
	async def send_pset(self,ctx):
		try:
			data = self.db.fetch_all_mashup()
			tz = pytz.timezone('Asia/Kolkata')
			time_day = datetime.now(tz).day
			time_month = datetime.now(tz).month
			time_year = datetime.now(tz).year
			for x in data:
				guildid = int(x[1])
				channelid = int(x[2])
				timelimit = int(x[3])*24*60*60
				lower_rating = int(x[4])
				last_sent  = int(x[5])
				upper_rating = int(x[6])
				problem_count= int(x[7])
				print(guildid,channelid,timelimit,lower_rating,last_sent,upper_rating,problem_count)
				if int(time.time())<last_sent+timelimit:
					print("skipping")
					continue
				self.db.update_mashup(x[0])
				channel = self.client.get_channel(channelid)
				mashupData = cfmaster.getPset(lower_rating,upper_rating,problem_count)
				embed = discord.Embed(description=mashupData, color=self.getRandomColour())
				current_pset = await channel.send(f"```{x[3]} Day Problemset : {time_day}/{time_month}/{time_year} || TL - {x[3]} Days```\n\n",embed=embed)
				self.db.add_mashup_data(guildid,channelid,current_pset.id)
				pset_emojis = "🇦🇧🇨🇩🇪"
				for i in range(problem_count):
					await current_pset.add_reaction(pset_emojis[i])
			await ctx.send("```Finished Sending Mashups !```")
		except Exception as e:
			await ctx.send(f"```{str(e)}```")


	@commands.command(brief='Get ranklist for this server')
	@commands.has_role('ACM - Active/Coding')
	async def ranklist(self,ctx):
		try:
			guildid = ctx.message.guild.id
			data = self.db.fetch_mashup_data(guildid)
			ranklist = {}
			for y in data:
				channel = find(lambda x: x.id == int(y[2]),  ctx.message.guild.text_channels)
				message = await channel.fetch_message(int(y[3]))
				for x in message.reactions:
					users = await x.users().flatten()
					for z in users:
						if z.bot==False:
							username = z.name+"#"+z.discriminator
							if username in ranklist.keys():
								ranklist[username]+=1
							else:
								ranklist[username]=1
			ranklist =dict(sorted(ranklist.items(), key=lambda item: item[1],reverse=True))
			style = table.Style('{:>} {:<} {:<}')
			t = table.Table(style)
			t += table.Header('No','Username', 'Solves')
			t += table.Line()
			idx = 1
			for x in ranklist:
				t += table.Data(idx,x, ranklist[x])
				idx+=1
			ranklist = '```yaml\n'+str(t)+'\n```'
			data = discord.Embed(title=f'Mashup Leaderboard',description=ranklist,color=self.getRandomColour())
			await ctx.send(embed=data)
		except Exception as e:
			await ctx.send(f"```{str(e)}```")

	@commands.command(brief='Get bot version')
	async def version(self,ctx):
		await ctx.send("```Version 1.5```")
	

def setup(client):
	client.add_cog(Mashups(client))
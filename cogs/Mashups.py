import discord
from discord.ext import commands, tasks
from discord.utils import find
import asyncio
import json
import requests
import random
import time
from .utils import cfmaster,db,table
import pytz
from datetime import datetime

RANKLIST_TIMELIMIT = 12*60*60

class Mashups(commands.Cog):
	"""docstring for FunStuff"""
	def __init__(self, client):
		self.client = client
		self.db = db.DB()
		self.printer.start()


	@commands.Cog.listener()
	async def on_ready(self):
		print("Daily PSet Online")

	@tasks.loop(seconds=300)
	async def printer(self):
		await self.send_pset_scheduled()


	@printer.before_loop
	async def before_printer(self):
		print('waiting...')
		await self.client.wait_until_ready()


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
	@commands.command(brief='Add a ranklist channel')
	async def add_ranklist(self,ctx):
		last_msg = ctx.channel.last_message
		await last_msg.delete()
		data = self.db.fetch_ranklist(str(ctx.guild.id))
		if data == None:
			self.db.add_ranklist(str(ctx.guild.id),str(ctx.channel.id))
			await ctx.send(f"```Ranklist assigned to this channel!```")
		else:
			self.db.update_ranklist(str(ctx.guild.id),str(ctx.channel.id))
			await ctx.send(f"```Ranklist channel updated```")
	
	@commands.has_role('Admin')
	@commands.command(brief='Add a static ranklist channel')
	async def add_static_ranklist(self,ctx):
		last_msg = ctx.channel.last_message
		await last_msg.delete()
		data = self.db.fetch_static_ranklist(str(ctx.guild.id))
		if data == None:
			data = await self.getRanklistEmbed(ctx.guild.id)
			msg = await ctx.send(embed=data)
			self.db.add_static_ranklist(str(ctx.guild.id),str(ctx.channel.id),str(msg.id))
			await ctx.send(f"```Static Ranklist assigned to this channel!```")
		else:
			await ctx.send(f"```Static Ranklist Already Exists```")

	@commands.has_role('Admin')
	@commands.command(brief='Initialize a Problemset')
	async def add_pset(self,ctx,lower_rating=None,upper_rating=None,time_limit=None,problem_count=None):
		last_msg = ctx.channel.last_message
		await last_msg.delete()
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
			if old_data != None:
				await ctx.send("```There already exist a mashup for this channel with same parameters```")	
				return
			self.db.add_mashup(guildid,channelid,time_limit,lower_rating,upper_rating,problem_count)			
			await ctx.send("```Assigned a mashup to this channel```")
		except Exception as e:
			await ctx.send(f"```In add_pset - {str(e)}```")

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
				guildid = int(x['guildid'])
				channelid = int(x['channelid'])
				timelimit = int(x['mashuptype'])*24*60*60
				lower_rating = int(x['lower_rating'])
				last_sent  = int(x['last_sent'])
				upper_rating = int(x['upper_rating'])
				problem_count= int(x['problem_count'])
				print(guildid,channelid,timelimit,lower_rating,last_sent,upper_rating,problem_count)
				if int(time.time())<last_sent+timelimit:
					print("skipping")
					continue
				self.db.update_mashup(x['id'])
				channel = self.client.get_channel(channelid)
				mashupData = cfmaster.getPset(lower_rating,upper_rating,problem_count)
				embed = discord.Embed(description=mashupData, color=self.getRandomColour())
				current_pset = await channel.send(f"```{x['mashuptype']} Day Problemset : {time_day}/{time_month}/{time_year} || TL - {x['mashuptype']} Days```\n\n",embed=embed)
				self.db.add_mashup_data(guildid,channelid,current_pset.id)
				pset_emojis = "🇦🇧🇨🇩🇪"
				for i in range(problem_count):
					await current_pset.add_reaction(pset_emojis[i])
			await ctx.send("```Finished Sending Mashups !```")
		except Exception as e:
			await ctx.send(f"```{str(e)}```")

	async def send_pset_scheduled(self):
		print("Here")
		try:
			data = self.db.fetch_all_mashup()			
			if len(data)==0:
				print("No Mashups")
			tz = pytz.timezone('Asia/Kolkata')
			time_day = datetime.now(tz).day
			time_month = datetime.now(tz).month
			time_year = datetime.now(tz).year
			for x in data:
				guildid = int(x['guildid'])
				channelid = int(x['channelid'])
				timelimit = int(x['mashuptype'])*24*60*60
				lower_rating = int(x['lower_rating'])
				last_sent  = int(x['last_sent'])
				upper_rating = int(x['upper_rating'])
				problem_count= int(x['problem_count'])
				print(guildid,channelid,timelimit,lower_rating,last_sent,upper_rating,problem_count)
				if int(time.time())<last_sent+timelimit:
					print("skipping")
					continue
				self.db.update_mashup(x['id'])
				channel = self.client.get_channel(channelid)
				mashupData = cfmaster.getPset(lower_rating,upper_rating,problem_count)
				embed = discord.Embed(description=mashupData, color=self.getRandomColour())
				current_pset = await channel.send(f"```{x['mashuptype']} Day Problemset : {time_day}/{time_month}/{time_year} || TL - {x['mashuptype']} Days```\n\n",embed=embed)
				self.db.add_mashup_data(guildid,channelid,current_pset.id)
				pset_emojis = "🇦🇧🇨🇩🇪"
				for i in range(problem_count):
					await current_pset.add_reaction(pset_emojis[i])
			print("Finished Sending Mashups ")
		except Exception as e:
			print(str(e))

		try:
			data = self.db.fetch_all_ranklist()
			if len(data)==0:
				print("No Ranklist")
			for x in data:
				pid = x['id']
				guildid = int(x['guildid'])
				channelid = int(x['channelid'])
				last_sent = int(x['last_sent'])
				if time.time()>int(last_sent)+RANKLIST_TIMELIMIT:
					await self.send_ranklist(str(guildid),str(channelid))
					self.db.update_ranklist_last_sent(str(pid))
				else:
					print("Skipping")
		except Exception as e:
			print(str(e))

		try:
			data = self.db.fetch_all_static_ranklist()
			if len(data)==0:
				print("No Static Ranklist")
			for x in data:
				pid = x['id']
				guildid = int(x['guildid'])
				channelid = int(x['channelid'])
				msgid = int(x['msg'])
				last_sent = int(x['last_updated'])
				data = await self.getRanklistEmbed(guildid)
				if time.time()>int(last_sent)+RANKLIST_TIMELIMIT:
					static_ranklist_channel = self.client.get_channel(channelid)
					msg = await static_ranklist_channel.fetch_message(msgid)					
					last_seen = int(time.time())-last_sent
					last_seen/=60
					last_seen/=60
					await msg.edit(content=f'Last Updated : {last_sent} hrs ago', embed=data)
					self.db.update_static_ranklist_last_sent(str(pid))
				else:
					print("Skipping")
		except Exception as e:
			print(str(e))


	@commands.command(brief='Get ranklist for this server')
	@commands.has_role('ACM - Active/Coding')
	@commands.has_role('Admin')
	async def ranklist(self,ctx):
		last_msg = ctx.channel.last_message
		await last_msg.delete()
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

	async def getRanklistEmbed(self,guildid):
		data = self.db.fetch_mashup_data(int(guildid))
		ranklist = {}
		for y in data:
			channel = self.client.get_channel(int(y['channelid']))
			message = await channel.fetch_message(int(y['msgid']))
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
		return data

	async def send_ranklist(self,guildid,channelid):
		data = await self.getRanklistEmbed(guildid)
		ranklist_channel = self.client.get_channel(int(channelid))
		await ranklist_channel.send(embed=data)
		


	@commands.command(brief='Get bot version')
	async def version(self,ctx):
		await ctx.send("```Version 2.0```")
	

def setup(client):
	client.add_cog(Mashups(client))
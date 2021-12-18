import discord
from discord.ext import commands
import asyncio
from discord.utils import find
import os

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix= 'e;', intents = intents)



@client.event
async def on_ready():
	print("Bot is Ready")
	cnt = 0
	for g in client.guilds:
		cnt += len(g.members)
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f"Codeforces Rounds with LGMs"))


@client.event
async def on_guild_join(guild):
	general = find(lambda x: x.name == 'general',  guild.text_channels)
	if general and general.permissions_for(guild.me).send_messages:
		desc += "\n\nI am a bot created by [s59_60r](https://github.com/s-i-d-d-i-s)"
		desc += "\n\nI help other coders in their training. By making mashups, track progress and asking random questions etc."
		desc += "\n\nI'm currently in beta.:frowning: "
		desc += "\n\nCheck Siddharth's [Github](https://github.com/s-i-d-d-i-s) to get updates on this Project and contribute"
		embed = discord.Embed(description=desc, color=discord.Colour(0xffff00))
		await general.send(embed=embed)


##################### Load Cogs ######################

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension("cogs.{}".format(filename.replace('.py','').strip()))




@client.event
async def on_member_join(member):
	print(f'{member} has joined our kitchen named {member.guild}!')



@client.event
async def on_member_remove(member):
	print(f'{member} has left our named {member.guild}!')


#Add Your Bot Token
token = os.getenv("BOT_TOKEN","TOKEN_")


client.run(token)
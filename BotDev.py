import discord,os
from discord.ext import commands
import json


#TOKEN = os.environ['token']

client = commands.Bot(command_prefix = "a!")


@client.event
async def on_ready():
	print("Logged in as {} {}".format(client.user.name,client.user.id))
	await client.change_presence(status = discord.Status.online,activity=discord.Game(name="Tech Support"))



# Load extensions
extensions = ['cogs.dffoo','cogs.admin']
if __name__ == '__main__':
	for extension in extensions:
		try:
			client.load_extension(extension)
		except Exception as e:
			print("{} cannot be loaded [{}]".format(extension,e))


client.run('MzM4MTA0ODgzNzkyMzE0Mzc5.XLaKKQ.ns7op8Ctv-K2Zbaarb6AWkS1PSM')

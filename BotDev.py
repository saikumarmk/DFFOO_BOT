import discord,os
from discord.ext import commands
import json
# Caution: This only works on python 3.7 + 
# In addition, you must run the semi - official build

TOKEN = os.environ['token']

client = commands.Bot(command_prefix = "a!")
client.remove_command('help')
# What is an event?
# An event is an action that happens inside discord
# The bot can see this and react in some way, with the functions we define for it.

@client.event
async def on_ready():
	print("Logged in as {} {}".format(client.user.name,client.user.id))
	await client.change_presence(status = discord.Status.online,activity=discord.Game(name="Tech Support"))

# Load extensions
'''
extensions = ['Cogs']
if __name__ == '__main__':
	for extension in extensions:
		try:
			client.load_extension(extension)
		except Exception as e:
			print("{} cannot be loaded [{}]".format(extension,e))
'''
#client.load_extension("cogs.dffooCog")


# A command tells the bot to do specific things
# What does context mean?
# It essentially tells the bot how the message was sent, and various details

# With contexts, they are an object so we can access their properties:
'''
context.message.channel
context.message.content
context.message.author
context.message.reactions
etc
Full link here:
https://discordpy.readthedocs.io/en/rewrite/api.html#discord.Message
'''


@client.command()
async def clean(context,amount=10):
	'''
	Usage is clean(amount of messages to be deleted)
	'''
	channel = context.message.channel
	messages = []
	# Context.history(limit=wahtaever)
	async for message in context.history(limit=amount+1):
		messages.append(message)
	await channel.delete_messages(messages)
	await context.send("{} messages deleted.".format(str(amount)))
	# Text.Channel.delete_messages 

@client.command()
async def ping(context):
	await context.send("pong")

# What does *args mean?
# It takes in as much arguments as supplied
# The first argument must ALWAYS be context

@client.command()
async def echo(context,*args):
	# If the person says @echo hi my name
	# The *args will be a tuple (hi,my,name)
	# We can conver this into a string like so:
	out = ",".join([word for word in args])
	print(args)
	# The join line converts the input to a string then joins using commas
	await context.send(out)

@client.command()
async def assd(context):
	await client.close()



client.run(TOKEN)


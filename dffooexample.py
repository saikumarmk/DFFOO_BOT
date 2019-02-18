
import discord
from discord.ext import commands
# Caution: This only works on python 3.7 + 
# In addition, you must run the semi - official build

token = 'MzM4MTA0ODgzNzkyMzE0Mzc5.D0tbVQ.soPQLBUplcogZQTLNp6sR8AY3Bo'
client = commands.Bot(command_prefix = "@")

# What is an event?
# An event is an action that happens inside discord
# The bot can see this and react in some way, with the functions we define for it.

@client.event
async def on_ready():
	print("Logged in as {} {}".format(client.user.name,client.user.id))
	await client.change_presence(status = discord.Status.online,activity=discord.Game(name="Tech Support"))



# A command tells the bot to do specific things
# What does context mean?
# It essentially tells the bot how the message was sent, and various details

@client.command()
async def clean(context,amount=10):
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
async def add(context,arg1,arg2):
	try:
		a,b = int(arg1),int(arg2)
	except ValueError:
		await context.send("Those aren't numbers!")
	else:
		await context.send("{}".format(str(a+b)))

# Embedding

@client.command()
async def unit(context,characterName):
	e = discord.Embed(
		title = 'Insert character names',
		description = 'This is a description'
		#colour = discord.Colour.red(),

		)
	e.set_footer(text = 'this a footer')
	e.set_image(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/facebook/138/thinking-face_1f914.png')
	e.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/facebook/138/thinking-face_1f914.png")
	#embed.set_author(name="MEE",icon_url="wahtever")
	e.add_field(name="Cool stuff from us",value="this is a thing",inline=True)
	e.add_field(name="Something",value="Woah",inline=True)
	e.add_field(name="Else",value="Amazed!",inline=True)
	await context.send(embed=e)

@client.command()
async def stop(context):
	await client.close()

client.run(token)


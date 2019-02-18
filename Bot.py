import discord
from discord.ext import commands
import json
# Caution: This only works on python 3.7 + 
# In addition, you must run the semi - official build

token = 'MzM4MTA0ODgzNzkyMzE0Mzc5.D0ulJw.GNa3E_wf3tCs0wxjhDSQJGdi-zM'
client = commands.Bot(command_prefix = "@")

# What is an event?
# An event is an action that happens inside discord
# The bot can see this and react in some way, with the functions we define for it.

@client.event
async def on_ready():
	print("Logged in as {} {}".format(client.user.name,client.user.id))
	await client.change_presence(status = discord.Status.online,activity=discord.Game(name="Tech Support"))


chars = json.loads(open('dependencies/charnames.json','r',encoding='utf-8').read())

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
	try:
		name = chars[characterName]
	except KeyError:
		await context.send("Character not found")
	else:
		charinfo = json.loads(open('dependencies/'+name+'.json','r',encoding='utf-8').read())
		e = discord.Embed(
			title = charinfo['Name'],
			#colour = discord.Colour.red(),

			)
		e.set_thumbnail(url=charinfo['Picture'])
		e.add_field(name="Crystal Color",value=charinfo['Crystal'],inline=True)
		e.add_field(name="Weapon Class",value=charinfo['Weapon'], inline=True)
		e.add_field(name="Stats",value=charinfo['Stats'],inline=True)
		e.add_field(name="Commands",value=charinfo['Commands'],inline=True)
		e.add_field(name="Enhancer 15CP",value="Raises targets BRV by 1/2 of Initial BRV when Shining Shield is used.",inline=False)
		e.add_field(name="Flame Sword 35CP",value="Increases the potency of Throw Buckler. Grants Small Initial BRV Up and Debuff Evasion Rate Up for 3 turns.",inline=True)
		e.add_field(name="Ice Brand 70CP",value="May equip the EX Ability Shining Wave.",inline=True)
		e.add_field(name="Crystal Shield 35CP",value="INT BRV+110 and DEF+84",inline=False)
		e.add_field(name="Shining Shield",value="Target: 5 turns Shield (reduces damage equal to own INT BRV ×2.3); 5 turns MAX BRV Up I; grants BRV ×1.5 High turn rate",inline=False)
		e.add_field(name="Throw Buckler", value="Ranged BRV attack High turn rate Draws target's attention for 5 turns with Lock Self: 5 turns Shield (reduces damage equal to own INT BRV ×2.3); 5 turns ATK Up I",inline=True)
		e.add_field(name="Shining Wave", value="2-hit ranged BRV attack + HP attack BRV damage increased based on total resistance value of party's active Shield effects Greatly restores party's HP based on HP damage dealt Recovery limit: 10% of MAX HP HP recovered in excess of MAX HP added to BRV Moderately increases SPD for 5 turns",inline=True)
		e.add_field(name="Top Passives", value="Class Change Boost 2 Star > Int Brv +170 > Mbrv +330", inline=False)
		e.set_footer(text="PLEASE NOTE: Passives are Kite's World Recommendations")
		await context.send(embed=e)

@client.command()
async def stop(context):
	await client.close()

client.run(token)


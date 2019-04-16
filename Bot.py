import discord,os
from discord.ext import commands
import json
# Caution: This only works on python 3.7 + 
# In addition, you must run the semi - official build


# DEPENDENCIES
chars = json.loads(open('dependencies/GL/charnames.json','r',encoding='utf-8').read())
Jchars = json.loads(open('dependencies/JP/charnames.json','r',encoding='utf-8').read())

colors = {
"Black":discord.Colour.default(),
"Blue":discord.Colour.blue(),
"Green":discord.Colour.green(),
"Red":discord.Colour.red(),
"White":discord.Colour.lighter_grey(),
"Yellow":discord.Colour.gold()}

passives = {}

with open("dependencies/OTHER/artifactpriority.csv") as w:
	for d in w.readlines():
		a = d.split(',')
		passives[a[0]] =[a[1],a[3],a[5]]
passives.pop('')


# Environment variables

#TOKEN = os.environ['token']
client = commands.Bot(command_prefix = "a!")
client.remove_command('help')
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

############################## MAIN COMMANDS

@client.command()
async def help(ctx,cmd):
	file = json.loads(open('dependencies/OTHER/helpcmd.json','r',encoding='utf-8').read())
	if not cmd:
		# general help command
		
		halp=discord.Embed(title='General functions',
							description='Use `!help `command` to find out more about them!')
		for i,j in file.items():
			halp.add_field(name=i,value=j,inline=False)
		#await ctx.message.add_reaction(emoji='✉')
		await ctx.send('',embed=halp)
	else:
		try:
			print(cmd)
			fn = file[cmd]

		except KeyError:
			await ctx.send("Command not found.")
		else:
			halp = discord.Embed(title=cmd,description=fn)
			await ctx.send('',embed=halp)

@client.command()
async def info(context,*characterName):
	'''	
	Usage is a!info <character name> and will return general information about a bot.
	'''		
	try:
		if len(characterName) == 1:
			nm = " ".join([f for f in characterName]).capitalize()
		else:
			nm = " ".join([f for f in characterName])
		name = chars[nm]
	except KeyError:
		await context.send("Character not found")
	else:

		charinfo = json.loads(open('dependencies/GL/'+name+'.json','r',encoding='utf-8').read())
		e = discord.Embed(
			title = charinfo['Name'],
			colour = colors[charinfo['Crystal']],

			)
		e.set_thumbnail(url=charinfo['Picture'])
		e.add_field(name="Crystal Color",value=charinfo['Crystal'],inline=True)
		#print(charinfo["Commands"])
		e.add_field(name="Weapon Class",value=charinfo['Weapon'], inline=True)
		#e.add_field(name="Stats",value=charinfo['Stats'],inline=True)
		#e.add_field(name="Commands",value=charinfo['Commands'],inline=True)
		try:
			for i in charinfo["Commands"].keys():
				e.add_field(name=i,value=charinfo["Commands"][i].replace("  "," "),inline=False)				
			topP = passives[nm]

		except KeyError:
			e.add_field(name="Recommended Passives",value="Not added",inline=False)
			await context.send(embed=e)
			
		else:
			for (i,j) in enumerate(topP):
				if not j:
					continue
				e.add_field(name="Passive {}".format(i+1),value=j,inline=False)
				e.set_footer(text="PLEASE NOTE: Passives are Kite's World Recommendations")
			await context.send(embed=e)
		

@client.command()
async def abilities(context,*characterName):
	'''
	Usage is a!abilities <character name> and will return command abilities.
	'''
	try:
		if len(characterName) == 1:
			nm = " ".join([f for f in characterName]).capitalize()
		else:
			nm = " ".join([f for f in characterName])
		name = chars[nm]
	except KeyError:
		await context.send("Character not found")
	else:

		charinfo = json.loads(open('dependencies/GL/'+name+'.json','r',encoding='utf-8').read())
		e = discord.Embed(
			title = charinfo['Name'],
			colour = colors[charinfo['Crystal']],
			)
		e.set_thumbnail(url=charinfo['Picture'])
		e.add_field(name="Crystal Color",value=charinfo['Crystal'],inline=True)
		e.add_field(name="Weapon Class",value=charinfo['Weapon'], inline=True)
		for i in charinfo["Commands"].keys():
			e.add_field(name=i,value=charinfo["Commands"][i].replace("  "," "),inline=False)

		await context.send(embed=e)


@client.command()
async def gear(context,*characterName):
	'''
	Usage is a!gear <character name> and returns all gear for a character
	'''
	try:
		if len(characterName) == 1:
			nm = " ".join([f for f in characterName]).capitalize()
		else:
			nm = " ".join([f for f in characterName])
		name = chars[nm]
	except KeyError:
		await context.send("Character not found")
	else:
		charinfo = json.loads(open('dependencies/GL/'+name+'.json','r',encoding='utf-8').read())
		e = discord.Embed(
			title = charinfo['Name'],
			colour = colors[charinfo['Crystal']],
			)
		e.set_thumbnail(url=charinfo['Picture'])
		e.add_field(name="Crystal Color",value=charinfo['Crystal'],inline=True)
		e.add_field(name="Weapon Class",value=charinfo['Weapon'], inline=True)
		for i in charinfo["Weapons"].keys():
			e.add_field(name=i,value=charinfo["Weapons"][i],inline=False)

		await context.send(embed=e)

@client.command()
async def stats(context,*characterName):
	'''
	Usage is a!stats <character name> and returns all stats for a character
	'''
	try:
		if len(characterName) == 1:
			nm = " ".join([f for f in characterName]).capitalize()
		else:
			nm = " ".join([f for f in characterName])
		name = chars[nm]
	except KeyError:
		await context.send("Character not found")
	else:
		charinfo = json.loads(open('dependencies/GL/'+name+'.json','r',encoding='utf-8').read())
		e = discord.Embed(
			title = charinfo['Name'],
			colour = colors[charinfo['Crystal']],
			)
		e.set_thumbnail(url=charinfo['Picture'])
		e.add_field(name="Crystal Color",value=charinfo['Crystal'],inline=True)
		e.add_field(name="Weapon Class",value=charinfo['Weapon'], inline=True)
		for i in charinfo["Stats"].keys():
			e.add_field(name=i,value=charinfo["Stats"][i],inline=False)

		await context.send(embed=e)

############################## JAPAN COMMANDS

@client.command()
async def Jinfo(context,*characterName):
	'''	
	Usage is a!info <character name> and will return general information about a bot.
	'''		
	try:
		if len(characterName) == 1:
			nm = " ".join([f for f in characterName]).capitalize()
		else:
			nm = " ".join([f for f in characterName])
		name = Jchars[nm]
	except KeyError:
		await context.send("Character not found")
	else:

		charinfo = json.loads(open('dependencies/JP/'+name+'.json','r',encoding='utf-8').read())
		e = discord.Embed(
			title = charinfo['Name'],
			colour = colors[charinfo['Crystal']],

			)
		e.set_thumbnail(url=charinfo['Picture'])
		e.add_field(name="Crystal Color",value=charinfo['Crystal'],inline=True)
		#print(charinfo["Commands"])
		e.add_field(name="Weapon Class",value=charinfo['Weapon'], inline=True)
		#e.add_field(name="Stats",value=charinfo['Stats'],inline=True)
		#e.add_field(name="Commands",value=charinfo['Commands'],inline=True)
		try:
			for i in charinfo["Commands"].keys():
				e.add_field(name=i,value=charinfo["Commands"][i].replace("  "," "),inline=False)				
			topP = passives[nm]

		except KeyError:
			e.add_field(name="Recommended Passives",value="Not added",inline=False)
			await context.send(embed=e)
			
		else:
			for (i,j) in enumerate(topP):
				if not j:
					continue
				e.add_field(name="Passive {}".format(i+1),value=j,inline=False)
				e.set_footer(text="PLEASE NOTE: Passives are Kite's World Recommendations")
			await context.send(embed=e)
		

@client.command()
async def Jabilities(context,*characterName):
	'''
	Usage is a!abilities <character name> and will return command abilities.
	'''
	try:
		if len(characterName) == 1:
			nm = " ".join([f for f in characterName]).capitalize()
		else:
			nm = " ".join([f for f in characterName])
		name = Jchars[nm]
	except KeyError:
		await context.send("Character not found")
	else:

		charinfo = json.loads(open('dependencies/JP/'+name+'.json','r',encoding='utf-8').read())
		e = discord.Embed(
			title = charinfo['Name'],
			colour = colors[charinfo['Crystal']],
			)
		e.set_thumbnail(url=charinfo['Picture'])
		e.add_field(name="Crystal Color",value=charinfo['Crystal'],inline=True)
		e.add_field(name="Weapon Class",value=charinfo['Weapon'], inline=True)
		for i in charinfo["Commands"].keys():
			e.add_field(name=i,value=charinfo["Commands"][i].replace("  "," "),inline=False)

		await context.send(embed=e)


@client.command()
async def Jgear(context,*characterName):
	'''
	Usage is a!gear <character name> and returns all gear for a character
	'''
	try:
		if len(characterName) == 1:
			nm = " ".join([f for f in characterName]).capitalize()
		else:
			nm = " ".join([f for f in characterName])
		name = Jchars[nm]
	except KeyError:
		await context.send("Character not found")
	else:
		charinfo = json.loads(open('dependencies/JP/'+name+'.json','r',encoding='utf-8').read())
		e = discord.Embed(
			title = charinfo['Name'],
			colour = colors[charinfo['Crystal']],
			)
		e.set_thumbnail(url=charinfo['Picture'])
		e.add_field(name="Crystal Color",value=charinfo['Crystal'],inline=True)
		e.add_field(name="Weapon Class",value=charinfo['Weapon'], inline=True)
		for i in charinfo["Weapons"].keys():
			e.add_field(name=i,value=charinfo["Weapons"][i],inline=False)

		await context.send(embed=e)

@client.command()
async def Jstats(context,*characterName):
	'''
	Usage is a!stats <character name> and returns all stats for a character
	'''
	try:
		if len(characterName) == 1:
			nm = " ".join([f for f in characterName]).capitalize()
		else:
			nm = " ".join([f for f in characterName])
		name = Jchars[nm]
	except KeyError:
		await context.send("Character not found")
	else:
		charinfo = json.loads(open('dependencies/JP/'+name+'.json','r',encoding='utf-8').read())
		e = discord.Embed(
			title = charinfo['Name'],
			colour = colors[charinfo['Crystal']],
			)
		e.set_thumbnail(url=charinfo['Picture'])
		e.add_field(name="Crystal Color",value=charinfo['Crystal'],inline=True)
		e.add_field(name="Weapon Class",value=charinfo['Weapon'], inline=True)
		for i in charinfo["Stats"].keys():
			e.add_field(name=i,value=charinfo["Stats"][i],inline=False)

		await context.send(embed=e)


client.run('MzM4MTA0ODgzNzkyMzE0Mzc5.XKtLkQ.OxjjFF-0lrUEbDwPJHTcnEwYS0k')


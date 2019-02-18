import discord
from discord.ext import commands
import json

# Dependencies
chars = json.loads(open('dependencies/charnames.json','r',encoding='utf-8').read())
colors = {
"Black":discord.Colour.default(),
"Blue":discord.Colour.blue(),
"Green":discord.Colour.green(),
"Red":discord.Colour.red(),
"White":discord.Colour.lighter_grey(),
"Yellow":discord.Colour.gold()}

# Commands
class Commands:
	def __init__(self,client):
		self.client = client

	@commands.command()
	async def unit(self,context,characterName):
		'''
		Usage is a!unit <character name> and will return general information about a bot.
		'''		
		try:
			name = chars[characterName]
		except KeyError:
			await context.send("Character not found")
		else:
			charinfo = json.loads(open('dependencies/'+name+'.json','r',encoding='utf-8').read())
			e = discord.Embed(
				title = charinfo['Name'],
				colour = colors[charinfo['Crystal']],

				)
			e.set_thumbnail(url=charinfo['Picture'])
			e.add_field(name="Crystal Color",value=charinfo['Crystal'],inline=True)
			e.add_field(name="Weapon Class",value=charinfo['Weapon'], inline=True)
			#e.add_field(name="Stats",value=charinfo['Stats'],inline=True)
			#e.add_field(name="Commands",value=charinfo['Commands'],inline=True)
			for i in charinfo["Commands"].keys():
				e.add_field(name=i,value=charinfo["Commands"][i],inline=False)
			for i in charinfo["Weapons"].keys():
				e.add_field(name=i,value=charinfo["Weapons"][i],inline=False)
			'''
			e.add_field(name="Shining Shield",value="Target: 5 turns Shield (reduces damage equal to own INT BRV ×2.3); 5 turns MAX BRV Up I; grants BRV ×1.5 High turn rate",inline=False)
			e.add_field(name="Throw Buckler", value="Ranged BRV attack High turn rate Draws target's attention for 5 turns with Lock Self: 5 turns Shield (reduces damage equal to own INT BRV ×2.3); 5 turns ATK Up I",inline=True)
			e.add_field(name="Shining Wave", value="2-hit ranged BRV attack + HP attack BRV damage increased based on total resistance value of party's active Shield effects Greatly restores party's HP based on HP damage dealt Recovery limit: 10% of MAX HP HP recovered in excess of MAX HP added to BRV Moderately increases SPD for 5 turns",inline=True)
			e.add_field(name="Top Passives", value="Class Change Boost 2 Star > Int Brv +170 > Mbrv +330", inline=False)
			e.set_footer(text="PLEASE NOTE: Passives are Kite's World Recommendations")
			'''
			await context.send(embed=e)

	@commands.command()
	async def abilities(self,context,characterName):
		'''
		Usage is a!abilities <character name> and will return command abilities.
		'''
		try:
			name = chars[characterName]
		except KeyError:
			await context.send("Character not found")
		else:
			charinfo = json.loads(open('dependencies/'+name+'.json','r',encoding='utf-8').read())
			e = discord.Embed(
				title = charinfo['Name'],
				colour = colors[charinfo['Crystal']],
				)
			e.set_thumbnail(url=charinfo['Picture'])
			e.add_field(name="Crystal Color",value=charinfo['Crystal'],inline=True)
			e.add_field(name="Weapon Class",value=charinfo['Weapon'], inline=True)
			for i in charinfo["Commands"].keys():
				e.add_field(name=i,value=charinfo["Commands"][i],inline=False)

			await context.send(embed=e)

	@commands.command()
	async def artifacts(self,context,characterName):
		'''
		Usage is a!artifacts <character name> and returns artifact passives.
		'''		
		try:
			name = chars[characterName]
		except KeyError:
			await context.send("Character not found")
		else:
			charinfo = json.loads(open('dependencies/'+name+'.json','r',encoding='utf-8').read())
			e = discord.Embed(
				title = charinfo['Name'],
				colour = colors[charinfo['Crystal']],
				)
			e.set_thumbnail(url=charinfo['Picture'])
			e.add_field(name="Crystal Color",value=charinfo['Crystal'],inline=True)
			e.add_field(name="Weapon Class",value=charinfo['Weapon'], inline=True)
			for i in charinfo["Artifacts"].keys():
				e.add_field(name=i,value=charinfo["Artifacts"][i],inline=False)

			await context.send(embed=e)


	@commands.command()
	async def passives(self,context,characterName):
		'''
		Usage is a!passives <character name> and rerturns passive skills
		'''
		try:
			name = chars[characterName]
		except KeyError:
			await context.send("Character not found")
		else:
			charinfo = json.loads(open('dependencies/'+name+'.json','r',encoding='utf-8').read())
			e = discord.Embed(
				title = charinfo['Name'],
				colour = colors[charinfo['Crystal']],
				)
			e.set_thumbnail(url=charinfo['Picture'])
			e.add_field(name="Crystal Color",value=charinfo['Crystal'],inline=True)
			e.add_field(name="Weapon Class",value=charinfo['Weapon'], inline=True)
			for i in charinfo["Passives"].keys():
				e.add_field(name=i,value=charinfo["Passives"][i],inline=False)

			await context.send(embed=e)

	@commands.command()
	async def gear(self,context,characterName):
		'''
		Usage is a!gear <character name> and returns all gear for a character
		'''
		try:
			name = chars[characterName]
		except KeyError:
			await context.send("Character not found")
		else:
			charinfo = json.loads(open('dependencies/'+name+'.json','r',encoding='utf-8').read())
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

	@commands.command()
	async def stats(self,context,characterName):
		'''
		Usage is a!stats <character name> and returns all stats for a character
		'''
		try:
			name = chars[characterName]
		except KeyError:
			await context.send("Character not found")
		else:
			charinfo = json.loads(open('dependencies/'+name+'.json','r',encoding='utf-8').read())
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

def setup(client):
	client.add_cog(Commands(client))
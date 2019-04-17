import discord
from discord.ext import commands
import json

# Dependencies
chars = json.loads(open('data/GL/charnames.json','r',encoding='utf-8').read())
Jchars = json.loads(open('data/JP/charnames.json','r',encoding='utf-8').read())

COLORS = {
"Black":discord.Colour.default(),
"Blue":discord.Colour.blue(),
"Green":discord.Colour.green(),
"Red":discord.Colour.red(),
"White":discord.Colour.lighter_grey(),
"Yellow":discord.Colour.gold()}

PASSIVES = {}
with open("data/OTHER/artifactpriority.csv") as w:
	for d in w.readlines():
		a = d.split(',')
		PASSIVES[a[0]] =[a[1],a[3],a[5]]
PASSIVES.pop('')



def setup(client):
	client.add_cog(Commands(client))



# Commands
class Commands:
	def __init__(self,client):
		self.client = client


	# TODO: Add more ways of recognizing names
	def retrieveName(self,characterName,locale):
		try:
			if len(characterName) == 1:
				formattedName = " ".join([f for f in characterName]).capitalize()
			else:
				formattedName = " ".join([f for f in characterName])
			if locale == "JP":
				indexedName = Jchars[formattedName]
				return (indexedName,formattedName)
			else:
				indexedName = chars[formattedName]
				return (indexedName,formattedName)
		except KeyError:
			return "Character not found!","Character not found!"


	def basicUnitEmbed(self,characterName,locale):

		characterInformation = json.loads(open("data/{}/{}.json".format(locale,characterName),'r',encoding='utf-8').read())
		
		embed = discord.Embed(
			title = characterInformation['Name'],
			color= COLORS[characterInformation['Crystal']])
		
		embed.set_thumbnail(url=characterInformation['Picture'])
		embed.add_field(name="Crystal Color",value=characterInformation['Crystal'],inline=True)
		embed.add_field(name="Weapon Class",value=characterInformation['Weapon'],inline=True)
		return embed,characterInformation


	def addInformationFields(self,characterInfo,informationType,embed):
		for i in characterInfo[informationType].keys():
			embed.add_field(name=i,value=characterInfo[informationType][i].replace("  "," "),inline=False)	
		return embed


	@commands.command()
	async def info(self,context,*characterName):
		'''a!info [name]\nDisplays overall character information (e.g. crystal color, recommended passives).'''
		indexedName,displayName = self.retrieveName(characterName,"GL")
		if indexedName == "Character not found!":
			await context.send("Character not found!".format(characterName))

		else:
			embed,charinfo = self.basicUnitEmbed(indexedName,"GL")

			try:
				self.addInformationFields(charinfo,"Commands",embed)	
				topP = PASSIVES[displayName]

			except KeyError:
				embed.add_field(name="Recommended Passives",value="Not added",inline=False)
				await context.send(embed=embed)

			else:
				for (i,j) in enumerate(topP):
					if not j:
						continue
					embed.add_field(name="Passive {}".format(i+1),value=j,inline=False)
					embed.set_footer(text="PLEASE NOTE: Passives are Kite's World Recommendations")
				await context.send(embed=embed)
			

	@commands.command()
	async def abilities(self,context,*characterName):
		'''a!abilities [name]\nDisplays a description for each of a character's command abilities.'''
		indexedName,displayName = self.retrieveName(characterName,"GL")
		if indexedName == "Character not found!":
			await context.send("Character not found!".format(characterName))

		else:
			embed,charinfo = self.basicUnitEmbed(indexedName,"GL")
			self.addInformationFields(charinfo,"Commands",embed)	
			await context.send(embed=embed)


	@commands.command()
	async def gear(self,context,*characterName):
		'''a!gear [name]\nDisplays available character gear.'''
		indexedName,displayName = self.retrieveName(characterName,"GL")
		if indexedName == "Character not found!":
			await context.send("Character not found!".format(characterName))

		else:
			embed,charinfo = self.basicUnitEmbed(indexedName,"GL")
			self.addInformationFields(charinfo,"Weapons",embed)	
			await context.send(embed=embed)


	@commands.command()
	async def Jinfo(self,context,*characterName):
		'''a!Jinfo [name]\nDisplays overall JP character information.'''
		indexedName,displayName = self.retrieveName(characterName,"JP")
		if indexedName == "Character not found!":
			await context.send("Character not found!".format(characterName))

		else:
			embed,charinfo = self.basicUnitEmbed(indexedName,"JP")

			try:
				self.addInformationFields(charinfo,"Commands",embed)	
				topP = PASSIVES[displayName]

			except KeyError:
				embed.add_field(name="Recommended Passives",value="Not added",inline=False)
				await context.send(embed=embed)

			else:
				for (i,j) in enumerate(topP):
					if not j:
						continue
					embed.add_field(name="Passive {}".format(i+1),value=j,inline=False)
					embed.set_footer(text="PLEASE NOTE: Passives are Kite's World Recommendations")
				await context.send(embed=embed)			


	@commands.command()
	async def Jabilities(self,context,*characterName):
		'''a!Jabilities [name]\nDisplays a description for each of a character's command abilities.'''
		indexedName,displayName = self.retrieveName(characterName,"JP")
		if indexedName == "Character not found!":
			await context.send("Character not found!".format(characterName))

		else:
			embed,charinfo = self.basicUnitEmbed(indexedName,"JP")
			self.addInformationFields(charinfo,"Commands",embed)	
			await context.send(embed=embed)


	@commands.command()
	async def Jgear(self,context,*characterName):
		'''a!Jgear [name]\nDisplays available character gear.'''
		indexedName,displayName = self.retrieveName(characterName,"JP")
		if indexedName == "Character not found!":
			await context.send("Character not found!".format(characterName))

		else:
			embed,charinfo = self.basicUnitEmbed(indexedName,"JP")
			self.addInformationFields(charinfo,"Weapons",embed)	
			await context.send(embed=embed)

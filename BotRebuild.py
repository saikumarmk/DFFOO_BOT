import os
import discord
from discord.ext import commands

class Atma(commands.Bot):
	def __init__(self,token):
		self.token = token
		super().__init__(command_prefix="a!")
		self.load_cogs()

	def load_cogs(self):
		extensions = ['cogs.dffoo','cogs.admin']
		for extension in extensions:
			try:
				self.load_extension(extension)
			except Exception as e:
				print("{} cannot be loaded [{}]".format(extension,e))


	async def on_ready(self):
		print("Logged in as {} {}".format(self.user.name,self.user.id))
		await self.change_presence(status = discord.Status.online,activity=discord.Game(name="Tech Support"))

	def run(self):
		super().run(self.token)
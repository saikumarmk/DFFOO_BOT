import discord
from discord.ext import commands
import json


def setup(bot):
	bot.add_cog(Commands(bot))



# Commands
class Commands:
	def __init__(self,bot):
		self.bot = bot


	@commands.command()
	async def clean(self,context,amount=10):
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


	@commands.command()
	async def assd(self,context):
		await self.bot.close()
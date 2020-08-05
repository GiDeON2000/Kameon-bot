import discord
from discord.ext import commands
import json
import pymongo
from config import settings

bot = commands.Bot(commands_prefix = '!')

cluster = MongoClient("mongodb+srv://gideon:upitob32@cluster0.gy3lr.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = cluster["discord-bot"]
collection = db["main"]

@bot.event
async def on_ready():
	for guild in bot.guilds:
  		for member in guild.members:
  			if collection.count_documents({"_id": member.id}) == 0:
  				collection.insert_one({
  				"_id": member.id,
  				"name": member.name,
  				"rep": 0
  				})
	print('ok')

bot.run(token)

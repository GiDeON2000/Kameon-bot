import discord
from discord.ext import commands
import json
import pymongo
import os

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

@bot.command(aliases=["+rep", "+реп"])
async def plus_reputation_for_member(self, ctx, member: discord.Member):
    for x in collection.find({"_id": member.id}):
        reps = x["rep"] = x["rep"] + 1
        collection.update_one({"_id": member.id}, {"$set": {"rep": reps}})
        emb = discord.Embed(title = f'+rep for {member.mention}', color = 0x0000FF)
        await ctx.send(embed=emb)


@bot.command()
async def my_reps(self, ctx, member: discord.Member):
    res = collection.find({"_id": member.id})
    for i in res:
        await ctx.send(i["rep"])

token = os.environ.get('BOT_TOKEN')
bot.run(str(token))

import discord
from discord.ext import commands
import json
import pymongo
import os

bot = commands.Bot(command_prefix = '!')

cluster = pymongo.MongoClient("mongodb+srv://gideon:upitob32@cluster0.gy3lr.mongodb.net/<dbname>?retryWrites=true&w=majority")
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
  				"rep": 0,
                "lvl": 0,
                "xp": 0
  				})
	print('ok')

@bot.command(aliases=["+rep", "+реп"])
async def plus_reputation_for_member(ctx, member: discord.Member):
    for x in collection.find({"_id": member.id}):
        reps = x["rep"] = x["rep"] + 1
        collection.update_one({"_id": member.id}, {"$set": {"rep": reps}})
        emb = discord.Embed(description = f'+rep for {member.mention}', color = 0x0000FF)
        await ctx.send(embed=emb)


@bot.command()
async def my_reps(ctx, member: discord.Member):
    res = collection.find({"_id": member.id})
    for i in res:
        await ctx.send(i["rep"])

@bot.event
async def on_message(message):
    for x in collection.find({"id": message.author.id}):
        xps = x["xp"] = x["xp"] + 50
        collection.update_one({"_id": member.id}, {"$set": {"xp": xps}})
        if x["xp"] > 100:
            lvls = x["lvl"] = x["lvl"] + 1
            collection.update_one({"_id": member.id}, {"$set": {"lvl": lvls}})
            await ctx.send(f'Levelup! {x["lvl"]}')
    await bot.process_commands(message)



token = os.environ.get('BOT_TOKEN')
bot.run(str(token))

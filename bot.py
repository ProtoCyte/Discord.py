from discord.ext import commands
import discord 
import datetime

BOT_TOKEN = "MTE5MDQzNDEyNTI0MTM4OTEwNg.GgwjUx.PFN5M1p7IUjjFoRv2soFTrD_ifzrnMc9GF6xoM"


default_activity = discord.Activity(type = discord.ActivityType.listening, name = "your every move")

bot = commands.Bot(command_prefix="!",activity = default_activity, status = discord.Status.idle ,intents = discord.Intents.all())

@bot.event
async def on_ready():
    # print("Bot is online")
    await bot.wait_until_ready()     
    print("Bot is ready")



# This gets the bot's current status
@bot.command()
async def currentstatus(ctx):
    current_activity = bot.activity
    print(f"Bot is currently {current_activity.name}")
    
# Deletes all messages in a channel (just for convenience)
@bot.command()
async def deleteall(ctx):
    await ctx.channel.purge()
    
    
    
    
bot.run(BOT_TOKEN)
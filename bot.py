from discord.ext import commands
import discord 
import datetime
from config import BOT_TOKEN
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
    channel = ctx.channel.name
    await ctx.channel.purge()
    await commandLogger("!deleteall", channel)
    
async def commandLogger(command_name = str, channel_name = str):
    channel = bot.get_channel(1190976583125700709)
    await channel.send(f"successfully ran {command_name} in {channel_name}")
    
    
    
bot.run(BOT_TOKEN)
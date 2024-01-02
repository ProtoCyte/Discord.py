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

# This gets the bot's current status with no reply
@bot.command()
async def currentstatus(ctx):
    current_activity = bot.activity
    await ctx.send(f"Bot is currently {default_activity.type.name} to {current_activity.name}")


# This changes the bot's current status
@bot.command()
async def changestatus(ctx,status):
    if (status == "idle"):
        await bot.change_presence(status = discord.Status.idle)
    elif (status == "online"):
        await bot.change_presence(status = discord.Status.online)
    elif (status == "offline"):
        await bot.change_presence(status = discord.Status.offline)
    elif (status == "dnd" | status == "do_not_disturb"):
        await bot.change_presence(status = discord.Status.dnd)
    elif (status == "invisible"):
        await bot.change_presence(status = discord.Status.invisible) 
    else: await ctx.send("Please choose a valid status")
        
# This changes what the bot activity is
@bot.command()
async def changeActivity(ctx, activity, activity_name):
    
    

# Deletes all messages in a channel (just for convenience)
@bot.command()
async def deleteall(ctx):
    channel = ctx.channel.name
    await ctx.channel.purge()
    await commandLogger("!deleteall", channel)




#Sends a message whenever a command is called, listing channel name and command
async def commandLogger(command_name = str, channel_name = str):
    channel = bot.get_channel(1190976583125700709)
    await channel.send(f"successfully ran {command_name} in {channel_name}")
    
    
    
bot.run(BOT_TOKEN)
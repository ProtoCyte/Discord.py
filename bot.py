from discord.ext import commands
import discord 
import asyncio
import speech_recognition as sr
from config import BOT_TOKEN


default_activity = discord.Activity(type = discord.ActivityType.listening, name = "your every move")

bot = commands.Bot(command_prefix="!",activity = default_activity, status = discord.Status.idle ,intents = discord.Intents.all())
recognizer = sr.Recognizer()
transcribing = False

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
async def botactivity(ctx, activitytype):
    valid_options = ["playing", "streaming","listening","watching"]
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel  
    if activitytype in valid_options:
        if (activitytype == "playing"):
            await ctx.reply("what would you like the bot to be playing")
            msg = await bot.wait_for("message", check = check)
            await bot.change_presence(activity = discord.Game(msg.content))
            return
        if (activitytype == "streaming"):
            await ctx.reply("what would you like the bot to be streaming")
            msg = await bot.wait_for("message", check = check)
            await ctx.reply("whats the url of the website")
            url = await bot.wait_for("message", check = check)
            await bot.change_presence(activity=discord.Streaming(name=msg.content, url=url.content))
            return
        if (activitytype == "listening"):
            await ctx.reply("what would you like the bot to be listening to")
            msg = await bot.wait_for("message", check = check)
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=msg.content))
            return
        if (activitytype == "watching"):
            await ctx.reply("what would you like the bot to be watching")
            msg = await bot.wait_for("message", check = check)
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=msg.content))
            return
    else: await ctx.reply("please pick a valid status")
          

# Deletes all messages in a channel (just for convenience)
@bot.command()
async def deleteall(ctx):
    channel = ctx.channel.name
    await ctx.channel.purge()
    await commandLogger("!deleteall", channel)

# Joins the call I'm in 
@bot.command()
async def joincall(ctx):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("please join a channel then retry command")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()
    
    await ctx.send(f"joined {channel.name}")

# leaves the call its currently in
@bot.command()
async def leavecall(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel")
    else:
        await ctx.send("I'm not in a voice channel")


#Sends a message whenever a command is called, listing channel name and command
async def commandLogger(command_name = str, channel_name = str):
    channel = bot.get_channel(1190976583125700709)
    await channel.send(f"successfully ran {command_name} in {channel_name}")
    
# This is the big part, this command listens to the user and what they are saying,
# it **should** be constant, but if it cannot be constant, it should be activated by a command, and 
# only disabled when a command tells it to stop listening
@bot.event
async def on_voice_state_update(member, before, after):
    global transcribing

    if member == bot.user and after.channel is not None:
        voice_channel = after.channel
        transcribing = True
        await bot.change_presence(activity=discord.Game(name="Transcribing"))

        try:
            # Run the transcription loop in a separate coroutine
            await transcribe_loop(voice_channel)

        except asyncio.CancelledError:
            pass
        
async def transcribe_loop(channel):
    global transcribing
    while transcribing:
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)  # Adjust timeout as needed
                text = recognizer.recognize_google(audio)
                print(f"Recognized: {text}")

                # Do something with the recognized text (e.g., send it to a channel)
                await channel.send(f"Live Transcription: {text}")

        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
        
@bot.command()
async def stoptranscription(ctx):
    global transcribing
    if transcribing:
        transcribing = False
        await ctx.send("stopped transcribing")    
    else:
        await ctx.send("not actively transcribing")
@bot.command()
async def continuetranscription(ctx):
    global transcribing
    if transcribing is False:
        transcribing = True
        await ctx.send("continuing transcribing")
    else:
        await ctx.send("not actively transcribing")
        

bot.run(BOT_TOKEN)
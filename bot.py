from discord.ext import commands
import discord 
import asyncio
import speech_recognition as sr
import openai, io
from gtts import gTTS
from config import BOT_TOKEN
from config import OPENAI_PERSONAL_KEY


default_activity = discord.Activity(type = discord.ActivityType.listening, name = "your every move")

bot = commands.Bot(command_prefix="!",activity = default_activity, status = discord.Status.idle ,intents = discord.Intents.all())
openai.api_key =  OPENAI_PERSONAL_KEY

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
@bot.command()
async def listen(ctx):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("You need to be in a voice channel to use this command.")
        return
    try:
        await ctx.send("Listening for speech...")

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=15)

        text = recognizer.recognize_google(audio)
        await ctx.send(f"Transcription: {text}")
        gpt_response = await sendtoGPT(text)
        await ctx.send(f"OpenAI response: {gpt_response}")
        await playtts(gpt_response)
        ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="speech.mp3"))
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
            
        
    except sr.UnknownValueError:
        await ctx.send("Sorry, I could not understand the speech.")

    except sr.RequestError as e:
        await ctx.send(f"Speech recognition request failed: {e}")

# Sends a message and returns a response from openai.
# Note this action costs money
async def sendtoGPT(text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= [
            {"role": "system", "content": "You are an assistant that is trying to help me defuse bombs in the game 'Keep Talking and Nobody Explodes'"},
            {"role": "user", "content": f"{text}"},
        ]
    )
    return response.choices[0].message.content
        
async def playtts(text):
    tts = gTTS(text= text, lang='en')
    tts.save("speech.mp3")
    
    
    
           

bot.run(BOT_TOKEN)
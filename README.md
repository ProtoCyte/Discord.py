# Keep Talking And Nobody Explodes Discord Bot
This is a Discord bot that is able to play the game "Keep Talking and Nobody Explodes." While it also has other features in the code, many of them were there purely for learning the *Discord API*. The most important functions are `!listen` and `!joincall`, as these are the 2 commands that activate the bot to play Keep Talking and Nobody Explodes.

It utilizes speech to text via the *Speech Recognition API*, *OpenAI* to generate respones, and then text to speech with *FFMPEG* to maintain conversation with the user, it also maintains all previous user responses and openAI responses, so that you should not have to restate anything.

There are a few things you will need to run the bot after downloading the repository.
1. A Discord Bot Token
2. An OpenAI Token
3. A working microphone

Once you have replaced both the **BOT_TOKEN** and **OPENAI_PERSONAL_KEY** with your own personal keys and tokens, run the bot with 

`python bot.py`

Then join a voice channel on discord of your choosing, and type `!joincall` in a text channel and the bot will join your call. Afterwards, when you are ready to play, type `!listen` and the bot will transcribe what you are saying, in addition to send a response from OpenAI and voice back the response as well.

The bot is configured to play "Keep Talking and Nobody Explodes", but it can likely also become a normal chatbot. Edit the code on line 16 that states `messages.append({"role": "system", "content": "You are an assistant that is trying to help me defuse bombs in the game 'Keep Talking and Nobody Explodes'"})` with any message after `"content"` with what you want the bot to know before you call `!listen` for the first time.

### Example of the bot working
![Example of command being called, and the response back](https://imgur.com/a/NPaCOuP)

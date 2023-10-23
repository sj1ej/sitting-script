import discord
from discord.ext import commands
import asyncio
import schedule

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Set the path to the Opus library (replace with the actual path)
discord.opus.load_opus('/opt/homebrew/Cellar/opus/1.4/lib/libopus.0.dylib')

# Create a bot instance with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Your bot token (replace with your token)
TOKEN = 'MTE2MjMyMzIyNTk0NzE1MjQyNQ.GiGsmR.4R96q4tcJ4YO0gxKmK-KFeZ0A81zRjbh4Y5aHQ'

# Your audio URL
audio_url = "https://discourses.dhamma.org/oml/recordings/uuid/5432df67-d6c3-4c65-aa30-099f8226f043.mp3"

async def send_text_message():
    print("Sending message...")
    text_channel = bot.get_channel(902394206939643980)
    if text_channel:
        await text_channel.send("We will start the group sit in 15 mins. Have an equanimous session")
    else:
        print("Text channel not found.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # Get the voice channel you want to join (replace with your channel ID)
    channel = bot.get_channel(1161909315255406593)

    if channel:
        voice_client = await channel.connect()

        # Schedule the audio to start playing at 7:00 PM every day
        schedule.every().day.at("19:00").do(start_audio, voice_client)
    else:
        print("Voice channel not found")

    # Schedule the text message to be sent at 6:45 PM every day
    schedule.every().day.at("18:45:10").do(lambda: asyncio.create_task(send_text_message()))

    # Run the scheduling loop
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

def start_audio(voice_client):
    # Play audio when scheduled
    voice_client.play(discord.FFmpegPCMAudio(audio_url, executable='ffmpeg'))

# Run the bot
bot.run(TOKEN)

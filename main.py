import os
from datetime import datetime, timezone

import discord
from discord.ext import commands, tasks
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
key = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

nero_bot_id = 945683386100514827
lifetime_limit = 21600


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    await initial_message_check()
    regular_check.start()


async def initial_message_check():
    print("Performing initial message check...")
    for guild in bot.guilds:
        print(guild)
        for channel in guild.text_channels + guild.voice_channels:
            print(channel)
            try:
                async for message in channel.history(limit=None):
                    if message.author.id == nero_bot_id:
                        await message.delete()
            except discord.errors.Forbidden:
                print(f"Missing permissions in {channel.name} of {guild.name}")
            except Exception as e:
                print(f"An error occurred during the initial check: {e}")
    print("Initial message check completed.")


@tasks.loop(hours=6)
async def regular_check():
    print("Performing regular message check...")
    for guild in bot.guilds:
        print(guild)
        for channel in guild.text_channels + guild.voice_channels:
            print(channel)
            try:
                async for message in channel.history(limit=100):
                    current_time = datetime.now(timezone.utc)
                    message_lifetime = (current_time - message.created_at).total_seconds()
                    if message.author.id == nero_bot_id and message_lifetime > lifetime_limit:
                        await message.delete()
            except discord.errors.Forbidden:
                print(f"Missing permissions in {channel.name} of {guild.name}")
            except Exception as e:
                print(f"An error occurred during the regular check: {e}")
    print("Regular message check completed.")


bot.run(key)

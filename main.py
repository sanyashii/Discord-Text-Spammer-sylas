import sys

# --- PYTHON 3.13 FIX ---
try:
    import audioop
except ImportError:
    try:
        import audioop_lts as audioop
        sys.modules['audioop'] = audioop
    except ImportError:
        print("Error: You must run 'pip install audioop-lts' in your terminal!")
# -----------------------

import discord
from discord.ext import tasks
import asyncio
import random
from datetime import datetime

# === CONFIGURATION ===
TOKEN = 'MTA3OTc0OTkyNDI2NDA5OTg2MQ.GWktG5.9UP6qB4ZoTr0FM5L8jDv0dH1UZmg8aroWLT7jM'  # Keep the quotes
CHANNEL_ID = 1451648011565404271          # NO quotes (must be numbers)
COMMAND = "!work"
# =====================

class MySelfBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as: {self.user}')
        print(f'Bot is starting the 1-hour interval for channel: {CHANNEL_ID}')
        
        # Start the loop if it's not already running
        if not self.work_loop.is_running():
            self.work_loop.start()

    @tasks.loop(hours=1)
    async def work_loop(self):
        channel = self.get_channel(CHANNEL_ID)
        
        if channel:
            # Add a random delay (1-2 minutes) to avoid detection
            jitter = random.randint(1, 120)
            print(f"Waiting {jitter}s to look like a human...")
            await asyncio.sleep(jitter)

            # Optional: Show 'typing...' for 3 seconds
            async with channel.typing():
                await asyncio.sleep(3)

            await channel.send(COMMAND)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent: {COMMAND}")
        else:
            print(f"Error: Could not find Channel ID {CHANNEL_ID}. Make sure the ID is correct and you are in that server.")

    @work_loop.before_loop
    async def before_work_loop(self):
        await self.wait_until_ready()

client = MySelfBot()

try:
    client.run(TOKEN)
except discord.LoginFailure:
    print("Error: The Token you provided is invalid. Please get a fresh token.")
except Exception as e:

    print(f"An unexpected error occurred: {e}")

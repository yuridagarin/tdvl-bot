import discord
from discord.ext import commands
import asyncio
#import config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập với {bot.user}")

async def main():
    await bot.load_extension("cogs.nopquy")
    await bot.load_extension("cogs.help")
    await bot.load_extension("cogs.showquy")
    await bot.load_extension("cogs.notify_auto")
    await bot.load_extension("cogs.logquy")
    await bot.load_extension("cogs.baoloi")
    #await bot.start(config.TOKEN)  
asyncio.run(main())

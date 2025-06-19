# main.py
import discord
from discord.ext import commands
import asyncio
import config
from flask import Flask
import threading
import os

# Khởi tạo Flask server đơn giản
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Khởi tạo bot Discord
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
    await bot.start(config.TOKEN)

# Chạy Flask server ở thread phụ
threading.Thread(target=run_flask).start()

# Chạy bot trong thread chính
asyncio.run(main())
import discord
from discord.ext import commands
from cogs.memory import nopquy_data
from collections import defaultdict
from datetime import datetime
import os

class LoggerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def ghi_tong_quy_theo_ngay(self):
        today = datetime.now().strftime("%Y-%m-%d")
        totals = defaultdict(int)

        if today in nopquy_data:
            for uid, entries in nopquy_data[today].items():
                for entry in entries:
                    try:
                        amount = int(entry["amount"])
                        item = entry["item"]
                        totals[item] += amount
                    except ValueError:
                        continue

        os.makedirs("logs", exist_ok=True)
        filepath = f"logs/tong_quy_{today}.txt"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Tổng kết quỹ ngày {today}:\n")
            for item, amount in totals.items():
                f.write(f"- {item}: {amount}\n")
        print(f"✅ Ghi file: {filepath}")

    @commands.Cog.listener()
    async def on_ready(self):
        print("📂 LoggerCog đã sẵn sàng.")
        self.ghi_tong_quy_theo_ngay()

async def setup(bot):
    await bot.add_cog(LoggerCog(bot))
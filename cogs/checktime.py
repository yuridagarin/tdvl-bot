from discord.ext import commands
from datetime import datetime
from zoneinfo import ZoneInfo

class CheckTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="time")
    async def time(self, ctx):
        now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
        await ctx.send(f"🕒 Giờ Việt Nam: `{now.strftime('%Y-%m-%d %H:%M:%S')}`")

async def setup(bot):
    await bot.add_cog(CheckTime(bot))
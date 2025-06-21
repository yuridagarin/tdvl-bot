import discord
from discord.ext import commands
import datetime

class CheckTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="time", help="Xem thời gian hiện tại theo giờ hệ thống bot")
    async def check_time(self, ctx):
        now = datetime.datetime.now()  # Nếu muốn UTC thì dùng datetime.utcnow()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")

        embed = discord.Embed(title="🕒 Thời gian hiện tại", description=f"`{time_str}`", color=discord.Color.blue())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CheckTime(bot))
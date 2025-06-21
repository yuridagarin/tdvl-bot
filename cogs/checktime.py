import discord
from discord.ext import commands
import datetime

# Thời gian bắt đầu bot
start_time = datetime.datetime.utcnow()

class CheckTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="uptime", help="Xem thời gian bot đã online")
    async def uptime(self, ctx):
        now = datetime.datetime.utcnow()
        delta = now - start_time

        days, remainder = divmod(delta.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        uptime_str = f"{int(days)} ngày, {int(hours)} giờ, {int(minutes)} phút, {int(seconds)} giây"

        embed = discord.Embed(title="🕒 Bot Uptime", description=uptime_str, color=discord.Color.green())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CheckTime(bot))
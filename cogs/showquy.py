from discord.ext import commands
from cogs.memory import nopquy_data
import datetime
import discord

class ShowQuyCog(commands.Cog, name="📊 Thống kê Quỹ"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="xemquy")
    async def show_quy(self, ctx, member: discord.Member = None):
        if not nopquy_data:
            await ctx.send("⚠️ Không có dữ liệu nộp quỹ.")
            return

        result = ""

        if member:
            uid = str(member.id)
            found = False
            result += f"📌 **Chi tiết nộp quỹ của {member.mention}:**\n"

            for day, day_data in nopquy_data.items():
                if uid in day_data:
                    for entry in day_data[uid]:
                        result += f"• ID: {entry['id']} – {entry['amount']} {entry['item']} (Ngày {day})\n"
                        found = True

            if not found:
                await ctx.send(f"📭 {member.display_name} chưa nộp quỹ nào.")
                return
        else:
            result += "**📋 Chi tiết tất cả người đã nộp (theo ID):**\n"
            for day, day_data in nopquy_data.items():
                result += f"\n📅 **Ngày {day}:**\n"
                for uid, entries in day_data.items():
                    try:
                        user = await ctx.bot.fetch_user(int(uid))
                        name = user.display_name
                    except:
                        name = f"ID {uid}"
                    for entry in entries:
                        result += f"• {name} | ID: {entry['id']} – {entry['amount']} {entry['item']}\n"

        await ctx.send(result or "⚠️ Không có dữ liệu để hiển thị.")

async def setup(bot):
    await bot.add_cog(ShowQuyCog(bot))
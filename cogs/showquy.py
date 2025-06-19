from discord.ext import commands
from cogs.memory import nopquy_data, saved_messages
import discord
from collections import defaultdict

class ShowQuyCog(commands.Cog, name="📊 Thống kê Quỹ"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="xemquy")
    async def show_quy(self, ctx, member: discord.Member = None):
        guild_id = str(ctx.guild.id)

        if guild_id not in nopquy_data or not nopquy_data[guild_id]:
            await ctx.send("⚠️ Server này chưa có dữ liệu nộp quỹ.")
            return

        result = ""
        totals = defaultdict(int)

        if member:
            uid = str(member.id)
            found = False
            result += f"📌 **Chi tiết nộp/rút quỹ của {member.mention}:**\n"

            for day, day_data in nopquy_data[guild_id].items():
                if uid in day_data:
                    result += f"\n📅 **Ngày {day}:**\n"
                    for entry in day_data[uid]:
                        amount = int(entry['amount'])
                        item = entry['item']
                        totals[item] += amount
                        result += f"• Nộp – ID: {entry['id']} – {amount} {item}\n"
                        found = True

                    if saved_messages.get(guild_id, {}).get(day, {}).get(uid):
                        for msg in saved_messages[guild_id][day][uid]:
                            if "đã rút" in msg:
                                result += f"• {msg}\n"
                                found = True

            if not found:
                await ctx.send(f"📭 {member.display_name} chưa nộp hoặc rút quỹ nào trong server này.")
                return

            result += "\n\n📦 **Tổng cộng đã nộp:**\n"
            for item, amount in totals.items():
                result += f"• {item}: `{amount}`\n"

        else:
            result += "**📋 Chi tiết toàn bộ người đã nộp/rút quỹ trong server:**\n"
            for day, day_data in nopquy_data[guild_id].items():
                result += f"\n📅 **Ngày {day}:**\n"
                for uid, entries in day_data.items():
                    try:
                        user = await ctx.bot.fetch_user(int(uid))
                        name = user.display_name
                    except:
                        name = f"ID {uid}"

                    result += f"👤 **{name}**\n"
                    for entry in entries:
                        amount = int(entry['amount'])
                        item = entry['item']
                        totals[item] += amount
                        result += f"• Nộp – ID: {entry['id']} – {amount} {item}\n"

                    if saved_messages.get(guild_id, {}).get(day, {}).get(uid):
                        for msg in saved_messages[guild_id][day][uid]:
                            if "đã rút" in msg:
                                result += f"• {msg}\n"

            result += "\n\n📦 **Tổng cộng toàn bộ đã nộp:**\n"
            for item, amount in totals.items():
                result += f"• {item}: `{amount}`\n"

        await ctx.send(result or "⚠️ Không có dữ liệu để hiển thị trong server này.")

async def setup(bot):
    await bot.add_cog(ShowQuyCog(bot))
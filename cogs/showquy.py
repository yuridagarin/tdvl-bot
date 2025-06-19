from discord.ext import commands
from cogs.memory import nopquy_data, saved_messages
import discord
from collections import defaultdict
from datetime import datetime
import re

class ShowQuyCog(commands.Cog, name="📊 Thống kê Quỹ"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="xemquy")
    async def show_quy(self, ctx, *, args=None):
        guild_id = str(ctx.guild.id)
        member = None
        day = None

        # Tách các phần: có thể là @user, ngày hoặc cả 2
        if args:
            mentions = ctx.message.mentions
            if mentions:
                member = mentions[0]
                args = args.replace(f"<@{member.id}>", "").replace(f"<@!{member.id}>", "").strip()

            date_match = re.match(r"^\d{4}-\d{2}-\d{2}$", args)
            if date_match:
                day = args

        if guild_id not in nopquy_data or not nopquy_data[guild_id]:
            await ctx.send("⚠️ Không có dữ liệu nộp quỹ nào trong server này.")
            return

        result = ""
        totals = defaultdict(int)
        data = nopquy_data[guild_id]

        def get_user_name(uid):
            user = ctx.guild.get_member(int(uid))
            return user.display_name if user else f"ID {uid}"

        if member:
            uid = str(member.id)
            result += f"📌 **Chi tiết nộp/rút quỹ của {member.mention}:**\n"
            found = False

            for d, day_data in data.items():
                if day and d != day:
                    continue
                if uid in day_data:
                    result += f"\n📅 **Ngày {d}:**\n"
                    for entry in day_data[uid]:
                        amount = int(entry['amount'])
                        item = entry['item']
                        totals[item] += amount
                        result += f"• Nộp – ID: {entry['id']} – {amount} {item}\n"
                        found = True

                    if saved_messages.get(guild_id, {}).get(d, {}).get(uid):
                        for msg in saved_messages[guild_id][d][uid]:
                            if "đã rút" in msg:
                                result += f"• {msg}\n"
                                found = True

            if not found:
                await ctx.send(f"📭 {member.display_name} chưa nộp hoặc rút quỹ nào.")
                return

        else:
            result += "**📋 Chi tiết toàn bộ người đã nộp/rút quỹ:**\n"
            for d, day_data in data.items():
                if day and d != day:
                    continue
                result += f"\n📅 **Ngày {d}:**\n"
                for uid, entries in day_data.items():
                    name = get_user_name(uid)
                    result += f"👤 **{name}**\n"
                    for entry in entries:
                        amount = int(entry['amount'])
                        item = entry['item']
                        totals[item] += amount
                        result += f"• Nộp – ID: {entry['id']} – {amount} {item}\n"

                    if saved_messages.get(guild_id, {}).get(d, {}).get(uid):
                        for msg in saved_messages[guild_id][d][uid]:
                            if "đã rút" in msg:
                                result += f"• {msg}\n"

        if not result.strip():
            await ctx.send("⚠️ Không có dữ liệu để hiển thị.")
            return

        result += "\n\n📦 **Tổng cộng đã nộp:**\n"
        for item, amount in totals.items():
            result += f"• {item}: `{amount}`\n"

        await ctx.send(result)

async def setup(bot):
    await bot.add_cog(ShowQuyCog(bot))

import os
import uuid
import datetime
from discord.ext import commands
from cogs.memory import saved_messages, user_current_day, nopquy_data
import discord
import re
from collections import defaultdict

class NopQuyCog(commands.Cog, name="💸 Nộp quỹ"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nopquy")
    async def nop_quy(self, ctx, *, message: str):
        mentions = ctx.message.mentions
        if mentions:
            target_user = mentions[0]
            content = message.replace(f"<@{target_user.id}>", "").replace(f"<@!{target_user.id}>", "").strip()
        else:
            target_user = ctx.author
            content = message

        match = re.match(r"^(\d+)\s+(.+)", content)
        if not match:
            await ctx.send("⚠️ Vui lòng nhập đúng định dạng: `!nopquy [@user] <số lượng> <vật phẩm>`")
            return

        amount = int(match.group(1))
        item_name = match.group(2).strip()
        user_name = target_user.display_name
        user_id = str(target_user.id)
        day = datetime.datetime.now().strftime("%d-%m-%Y")


        if day not in nopquy_data:
            nopquy_data[day] = {}
        if user_id not in nopquy_data[day]:
            nopquy_data[day][user_id] = []


        file_dir = "data_quy"
        os.makedirs(file_dir, exist_ok=True)
        file_path = os.path.join(file_dir, f"{day}.txt")
        lines = []
        updated = False
        existing_id = None

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(" | ")
                    if len(parts) == 3:
                        name, amt_item, id_part = parts
                        if name == user_name and amt_item.endswith(item_name):
                            try:
                                old_amount = int(amt_item.split(" ")[0])
                                new_amount = old_amount + amount
                                existing_id = id_part.strip().replace("ID: ", "")
                                lines.append(f"{user_name} | {new_amount} {item_name} | ID: {existing_id}\n")
                                updated = True
                                continue
                            except:
                                pass
                    lines.append(line)

        if not updated:
            existing_id = str(uuid.uuid4())[:8]
            lines.append(f"{user_name} | {amount} {item_name} | ID: {existing_id}\n")

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)


        entry = {
            "id": existing_id,
            "amount": amount,
            "item": item_name,
            "name": user_name
        }
        nopquy_data[day][user_id].append(entry)

        if day not in saved_messages:
            saved_messages[day] = {}
        if user_id not in saved_messages[day]:
            saved_messages[day][user_id] = []

        saved_messages[day][user_id].append(f"Nộp quỹ [{existing_id}]: {amount} {item_name}")


        totals = defaultdict(int)
        for entry in nopquy_data[day][user_id]:
            totals[entry["item"]] += entry["amount"]

        total_lines = "\n".join([f"- {total} {item}" for item, total in totals.items()])
        await ctx.send(
            f"💰 Đã ghi nhận `{amount} {item_name}` cho `{user_name}` ngày `{day}` với ID `{existing_id}`.\n"
            f"📦 Tổng đã nộp trong ngày:\n{total_lines}"
        )

    @commands.command(name="xoaquy")
    async def delete_nopquy(self, ctx, member: discord.Member, *, content: str = None):
        user_id = str(member.id)
        user_name = member.display_name
        day = user_current_day.get(ctx.author.id, datetime.datetime.now().strftime("%d-%m-%Y"))

        if day not in nopquy_data or user_id not in nopquy_data[day]:
            await ctx.send(f"⚠️ Không có dữ liệu nộp quỹ của {member.mention} trong ngày `{day}`.")
            return

        entries = nopquy_data[day][user_id]

        if not content:

            del nopquy_data[day][user_id]
            if day in saved_messages and user_id in saved_messages[day]:
                del saved_messages[day][user_id]
            await ctx.send(f"🗑️ Đã xoá toàn bộ dữ liệu nộp quỹ của {member.mention} trong ngày `{day}`.")
            return

        match = re.match(r"^(\d+)\s+(.+)", content.strip())
        if not match:
            await ctx.send("❌ Cú pháp sai. Dùng: `!xoaquy @user 100 vàng` hoặc `!xoaquy @user` để xoá toàn bộ.")
            return

        amount_to_remove = int(match.group(1))
        item_name = match.group(2).strip().lower()

        new_entries = []
        removed = 0
        removed_ids = []

        for entry in entries:
            if entry["item"].lower() == item_name and removed < amount_to_remove:
                remaining = amount_to_remove - removed
                if entry["amount"] <= remaining:
                    removed += entry["amount"]
                    removed_ids.append(entry["id"])
                    continue 
                else:
                    entry["amount"] -= remaining
                    removed += remaining
                    removed_ids.append(entry["id"])
                    new_entries.append(entry)
            else:
                new_entries.append(entry)

        if removed == 0:
            await ctx.send(f"⚠️ Không tìm thấy vật phẩm `{item_name}` hoặc không đủ số lượng.")
            return


        nopquy_data[day][user_id] = new_entries
        saved_messages[day][user_id] = [
            f"Nộp quỹ [{e['id']}]: {e['amount']} {e['item']}" for e in new_entries
        ]


        file_dir = "data_quy"
        file_path = os.path.join(file_dir, f"{day}.txt")
        lines = []

        for uid, user_entries in nopquy_data[day].items():
            for e in user_entries:
                lines.append(f"{e['name']} | {e['amount']} {e['item']} | ID: {e['id']}\n")

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        await ctx.send(
            f"🗑️ Đã xoá `{removed}` đơn vị `{item_name}` khỏi dữ liệu của {member.mention} trong ngày `{day}`.\n"
            f"📌 ID bị ảnh hưởng: {', '.join(removed_ids)}"
        )
async def setup(bot):
    await bot.add_cog(NopQuyCog(bot))
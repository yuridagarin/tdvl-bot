import os
import uuid
import datetime
from discord.ext import commands
from cogs.memory import saved_messages, user_current_day, nopquy_data
import discord
import re
from collections import defaultdict
from ulti.logger import ghi_tong_quy_theo_ngay

class NopQuyCog(commands.Cog, name="💸 Nộp quỹ"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nopquy")
    async def nop_quy(self, ctx, *, message: str):
        guild_id = str(ctx.guild.id)
        guild_name = re.sub(r'[\\/*?:"<>|]', "_", ctx.guild.name)
        day = datetime.datetime.now().strftime("%Y-%m-%d")

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

        if guild_id not in nopquy_data:
            nopquy_data[guild_id] = {}
        if day not in nopquy_data[guild_id]:
            nopquy_data[guild_id][day] = {}
        if user_id not in nopquy_data[guild_id][day]:
            nopquy_data[guild_id][day][user_id] = []

        file_dir = os.path.join("data_quy", guild_name)
        os.makedirs(file_dir, exist_ok=True)
        file_path = os.path.join(file_dir, f"{day}.txt")

        existing_lines = []
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                existing_lines = f.readlines()

        lines = []
        updated = False
        existing_id = None

        for line in existing_lines:
            parts = line.strip().split(" | ")
            if len(parts) == 4:
                uid, name, amt_item, id_part = parts
                try:
                    old_amount_str, old_item_name = amt_item.strip().split(" ", 1)
                    if uid == user_id and old_item_name.strip().lower() == item_name.lower():
                        old_amount = int(old_amount_str)
                        new_amount = old_amount + amount
                        existing_id = id_part.strip().replace("ID: ", "")
                        lines.append(f"{user_id} | {user_name} | {new_amount} {item_name} | ID: {existing_id}\n")
                        updated = True
                        continue
                except:
                    pass
            lines.append(line)

        if not updated:
            existing_id = str(uuid.uuid4())[:8]
            lines.append(f"{user_id} | {user_name} | {amount} {item_name} | ID: {existing_id}\n")

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        entry = {
            "id": existing_id,
            "amount": amount,
            "item": item_name,
            "name": user_name
        }
        nopquy_data[guild_id][day][user_id].append(entry)

        if guild_id not in saved_messages:
            saved_messages[guild_id] = {}
        if day not in saved_messages[guild_id]:
            saved_messages[guild_id][day] = {}
        if user_id not in saved_messages[guild_id][day]:
            saved_messages[guild_id][day][user_id] = []

        saved_messages[guild_id][day][user_id].append(f"Nộp quỹ [{existing_id}]: {amount} {item_name}")

        totals = defaultdict(int)
        for entry in nopquy_data[guild_id][day][user_id]:
            totals[entry["item"]] += entry["amount"]

        total_lines = "\n".join([f"- {total} {item}" for item, total in totals.items()])
        await ctx.send(
            f"💰 Đã ghi nhận `{amount} {item_name}` cho `{user_name}` ngày `{day}` với ID `{existing_id}`.\n"
            f"📦 Tổng đã nộp trong ngày:\n{total_lines}"
        )
        ghi_tong_quy_theo_ngay(nopquy_data[guild_id], guild_name=guild_name)

    @commands.command(name="rutquy")
    async def delete_nopquy(self, ctx, member: discord.Member, *, content: str = None):
        guild_id = str(ctx.guild.id)
        guild_name = re.sub(r'[\\/*?:"<>|]', "_", ctx.guild.name)
        user_id = str(member.id)
        user_name = member.display_name
        day = user_current_day.get(ctx.author.id, datetime.datetime.now().strftime("%Y-%m-%d"))

        if guild_id not in nopquy_data or day not in nopquy_data[guild_id] or user_id not in nopquy_data[guild_id][day] or not nopquy_data[guild_id][day][user_id]:
            await ctx.send(f"⚠️ Không có dữ liệu nộp quỹ của {member.mention} trong ngày `{day}`.")
            return

        entries = nopquy_data[guild_id][day][user_id]

        if not content:
            del nopquy_data[guild_id][day][user_id]
            if guild_id in saved_messages and day in saved_messages[guild_id] and user_id in saved_messages[guild_id][day]:
                del saved_messages[guild_id][day][user_id]
            await ctx.send(f"🗑️ Đã xoá toàn bộ dữ liệu nộp quỹ của {member.mention} trong ngày `{day}`.")
        else:
            match = re.match(r"^(\d+)\s+(.+)", content.strip())
            if not match:
                await ctx.send("❌ Cú pháp sai. Dùng: `!rutquy @user 100 vàng` hoặc `!rutquy @user` để xoá toàn bộ.")
                return

            amount_to_remove = int(match.group(1))
            item_name = match.group(2).strip().lower()

            new_entries = []
            removed = 0
            removed_entries = []
            removed_ids = []

            for entry in entries:
                if entry["item"].lower() == item_name and removed < amount_to_remove:
                    remaining = amount_to_remove - removed
                    if entry["amount"] <= remaining:
                        removed += entry["amount"]
                        removed_entries.append(entry)
                        removed_ids.append(entry["id"])
                        continue
                    else:
                        entry["amount"] -= remaining
                        removed += remaining
                        removed_entries.append({"id": entry["id"], "amount": remaining, "item": entry["item"]})
                        removed_ids.append(entry["id"])
                        new_entries.append(entry)
                else:
                    new_entries.append(entry)

            if removed == 0:
                await ctx.send(f"⚠️ Không tìm thấy vật phẩm `{item_name}` hoặc không đủ số lượng.")
                return

            if new_entries:
                nopquy_data[guild_id][day][user_id] = new_entries
            else:
                del nopquy_data[guild_id][day][user_id]

            if guild_id not in saved_messages:
                saved_messages[guild_id] = {}
            if day not in saved_messages[guild_id]:
                saved_messages[guild_id][day] = {}
            saved_messages[guild_id][day][user_id] = [
                f"Nộp quỹ [{e['id']}]: {e['amount']} {e['item']}" for e in new_entries
            ]
            for e in removed_entries:
                saved_messages[guild_id][day][user_id].append(f"ID: {e['id']} – đã rút {e['amount']} {e['item']}")

            file_dir = os.path.join("data_quy", guild_name)
            os.makedirs(file_dir, exist_ok=True)
            file_path = os.path.join(file_dir, f"{day}.txt")

            entry_map = {}
            for uid, user_entries in nopquy_data[guild_id][day].items():
                for e in user_entries:
                    key = (uid, e["id"])
                    if key in entry_map:
                        entry_map[key]["amount"] += e["amount"]
                    else:
                        entry_map[key] = {
                            "uid": uid,
                            "name": e["name"],
                            "amount": e["amount"],
                            "item": e["item"],
                            "id": e["id"]
                        }

            lines = [
                f"{entry['uid']} | {entry['name']} | {entry['amount']} {entry['item']} | ID: {entry['id']}\n"
                for entry in entry_map.values()
            ]

            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            ghi_tong_quy_theo_ngay(nopquy_data[guild_id], guild_name=guild_name)

            await ctx.send(
                f"🗑️ Đã rút `{removed}` đơn vị `{item_name}` khỏi {member.mention} trong ngày `{day}`.\n"
                f"📌 ID bị ảnh hưởng: {', '.join(removed_ids)}"
            )

async def setup(bot):
    await bot.add_cog(NopQuyCog(bot))

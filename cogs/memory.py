from discord.ext import commands
import datetime

# Lưu tin nhắn dạng: { "dd-mm-yyyy": [msg1, msg2] }
saved_messages = {}
nopquy_data = {}
xoaquy_counter = {} 
# Ghi nhớ ngày hiện tại của mỗi người dùng: { user_id: "dd-mm-yyyy" }
user_current_day = {}

class MemoryCog(commands.Cog, name="📌 Bộ nhớ"):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="chonngay", help="Chọn ngày lưu tin nhắn (định dạng dd-mm-yyyy)")
    async def set_day(self, ctx, *, date_text=None):
        user_id = ctx.author.id
        if date_text:
            try:

                datetime.datetime.strptime(date_text, "%d-%m-%Y")
                user_current_day[user_id] = date_text
                await ctx.send(f"📅 Ngày đã chọn: `{date_text}`")
            except ValueError:
                await ctx.send("❌ Định dạng ngày không hợp lệ. Dùng: `!quỹ 18-06-2025`")
        else:

            today = datetime.datetime.now().strftime("%d-%m-%Y")
            user_current_day[user_id] = today
            await ctx.send(f"📅 Ngày mặc định được chọn: `{today}`")

    @commands.command(name="luuquy", help="Lưu lại tin nhắn vào ngày đã chọn")
    async def save_message(self, ctx, *, message: str):
        user_id = ctx.author.id
        day = user_current_day.get(user_id, datetime.datetime.now().strftime("%d-%m-%Y"))

        if day not in saved_messages:
            saved_messages[day] = []

        saved_messages[day].append(message)
        await ctx.send(f"💾 Đã lưu vào ngày `{day}`")

    @commands.command(name="dsquy", help="Hiển thị các tin nhắn đã lưu (mặc định hôm nay)")
    async def show_messages(self, ctx, *, date_text=None):
        if date_text:
            day = date_text
        else:
            day = user_current_day.get(ctx.author.id, datetime.datetime.now().strftime("%d-%m-%Y"))

        if day not in saved_messages or not saved_messages[day]:
            await ctx.send(f"⚠️ Không có tin nhắn nào được lưu cho ngày `{day}`.")
            return

        msg_list = saved_messages[day]
        msg = "\n".join(f"{i+1}. {m}" for i, m in enumerate(msg_list))
        await ctx.send(f"📋 Tin nhắn đã lưu cho ngày `{day}`:\n{msg}")

    @commands.command(name="delete", help="Xoá một tin nhắn đã lưu theo số thứ tự")
    async def delete_message(self, ctx, index: int):
        day = user_current_day.get(ctx.author.id, datetime.datetime.now().strftime("%d-%m-%Y"))

        if day not in saved_messages or not saved_messages[day]:
            await ctx.send("⚠️ Không có tin nhắn nào được lưu trong ngày này.")
            return

        messages = saved_messages[day]

        if index < 1 or index > len(messages):
            await ctx.send(f"❌ Số thứ tự không hợp lệ. Bạn chỉ có {len(messages)} tin nhắn.")
            return

        deleted = messages.pop(index - 1)
        await ctx.send(f"✅ Đã xoá tin nhắn số {index}: `{deleted}`")

        

async def setup(bot):
    await bot.add_cog(MemoryCog(bot))
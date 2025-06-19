from discord.ext import commands
import discord

class HelpCog(commands.Cog, name="❓ Hướng dẫn"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="huongdan", help="Hiển thị hướng dẫn sử dụng bot theo từng chức năng")
    async def guide(self, ctx):
        is_admin = discord.utils.get(ctx.author.roles, name="Thủ quỹ")

        if is_admin:
            help_text = """
💸 **Nộp quỹ (NopQuy):**
• `!nopquy <số_lần> <ghi chú>` – (Chỉ thủ quỹ) Ghi nhận số lần nộp quỹ và lưu nội dung.
• `!xoaquy @user` <số lượng> <vật phẩm> – (Chỉ thủ quỹ) Xoá quỹ nộp của cá nhân theo vật phẩm hoặc toàn bộ.

🕒 **Cài đặt thời gian:**
• `!settime Giờ:Phút <nội dung>` – (Chỉ thủ quỹ) Chỉnh thời gian sự kiện sẽ thông báo trong ngày

📊 **Thống kê :**
• `!xemquy` – Hiển thị tổng số lượt nộp quỹ của tất cả mọi người hoặc của bạn.

📖 **Hướng dẫn:**
• `!huongdan` – Hiển thị bảng hướng dẫn này.
"""
        else:
            help_text = """
📊 **Thống kê :**
• `!xemquy` – Hiển thị tổng số lượt nộp quỹ của tất cả mọi người hoặc của bạn.

📖 **Hướng dẫn:**
• `!huongdan` – Hiển thị bảng hướng dẫn này.
"""

        await ctx.send(help_text)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
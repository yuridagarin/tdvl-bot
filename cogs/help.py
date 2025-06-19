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
💸 **Nộp quỹ:**
• `!nopquy @ten <số_lượng> <vật phẩm>` – (Chỉ thủ quỹ) Ghi nhận số lượng nộp quỹ và lưu nội dung.
• `!rutquy @ten` <số lượng> <vật phẩm> – (Chỉ thủ quỹ) Xoá quỹ nộp của cá nhân theo vật phẩm hoặc toàn bộ.

🕒 **Cài đặt thời gian:**
• `!settime Giờ:Phút <nội dung>` – (Chỉ bang chủ và phó bang) Chỉnh thời gian sự kiện sẽ thông báo trong ngày.

📊 **Thống kê :**
• `!xemquy` @ten hoặc `!xemquy` – Hiển thị tổng số lượt nộp quỹ của người nào đó hoặc của bạtất cả trong ngày.

🛠️ **Báo lỗi Bot:**
• `!baoloi <nội dung lỗi>` – Gửi báo cáo lỗi tới quản trị viên, tự động tạo kênh xử lý riêng.

📖 **Hướng dẫn:**
• `!huongdan` – Hiển thị bảng hướng dẫn này.
"""
        else:
            help_text = """
📊 **Thống kê :**
• `!xemquy` – Hiển thị tổng số lượt nộp quỹ của tất cả mọi người hoặc của bạn.

🛠️ **Báo lỗi Bot:**
• `!baoloi <nội dung lỗi>` – Gửi báo cáo lỗi tới quản trị viên, chúng tôi sẽ hỗ trợ bạn sớm nhất.

📖 **Hướng dẫn:**
• `!huongdan` – Hiển thị bảng hướng dẫn này.
"""

        await ctx.send(help_text)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))

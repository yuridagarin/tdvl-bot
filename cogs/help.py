from discord.ext import commands

class HelpCog(commands.Cog, name="❓ Hướng dẫn"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="huongdan", help="Hiển thị hướng dẫn sử dụng bot theo từng chức năng")
    async def guide(self, ctx):
        help_text = """
💸 **Nộp quỹ (NopQuy):**
• `!nopquy <số_lần> <ghi chú>` – Ghi nhận số lần nộp quỹ và lưu nội dung
• `!xoaquy @user` – Xoá toàn bộ dòng nộp quỹ của người được tag trong ngày hiện tại

📊 **Thống kê :**
• `!xemquy` – Hiển thị tổng số lượt nộp quỹ của tất cả mọi người (gộp mọi ngày)

📖 **Hướng dẫn:**
• `!huongdan` – Hiển thị bảng hướng dẫn này
"""
        await ctx.send(help_text)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))

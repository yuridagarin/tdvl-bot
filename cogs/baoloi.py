import discord
from discord.ext import commands
import datetime

class BaoLoiCog(commands.Cog, name="🛠️ Báo lỗi"):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_counter = 0  # Để phân biệt nhiều ticket

@commands.command(name="baoloi")
async def bao_loi(self, ctx, *, content: str = None):
    if not content:
        await ctx.send("⚠️ Vui lòng nhập nội dung lỗi. Ví dụ: `!baoloi Bot không phản hồi khi dùng !help`")
        return

    guild = ctx.guild
    author = ctx.author
    self.ticket_counter += 1

    channel_name = f"ticket-{author.name.lower().replace(' ', '-')}-{self.ticket_counter}"
    category = discord.utils.get(guild.categories, name="tickets")

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }

    channel = await guild.create_text_channel(
        name=channel_name,
        overwrites=overwrites,
        category=category,
        topic=f"Ticket báo lỗi của {author.name}"
    )

    embed = discord.Embed(
        title="🛠️ Báo lỗi mới",
        description=content,
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_author(name=author.display_name, icon_url=author.display_avatar.url)

    await channel.send(f"{author.mention}, cảm ơn bạn đã báo lỗi! Vui lòng nếu có thể gửi video lỗi và ghi nội dung chi tiết lỗi rõ ràng nhất có thể.")
    await channel.send(embed=embed)

    await ctx.send(f"✅ Đã tạo ticket báo lỗi tại kênh {channel.mention}")

    # 📨 Gửi thông báo tới user cố định
    notify_user_id = 996715877309370408  # 🔁 Thay bằng ID người cần nhận thông báo
    notify_user = self.bot.get_user(notify_user_id)
    if notify_user:
        try:
            await notify_user.send(
                f"🔔 Có báo lỗi mới từ **{author}**:\n"
                f"Nội dung: {content}\n"
                f"Kênh: {channel.mention}"
            )
        except discord.Forbidden:
            print(f"Không thể gửi DM cho {notify_user}")
async def setup(bot):
    await bot.add_cog(BaoLoiCog(bot))
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

        # Tạo tên channel
        channel_name = f"ticket-{author.name.lower().replace(' ', '-')}-{self.ticket_counter}"

        # Optional: tìm category tên 'tickets' nếu có
        category = discord.utils.get(guild.categories, name="tickets")

        # Tạo channel với quyền riêng tư
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

        # Gửi nội dung lỗi vào channel
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

async def setup(bot):
    await bot.add_cog(BaoLoiCog(bot))
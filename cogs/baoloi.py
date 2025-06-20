import discord
from discord.ext import commands
import datetime
import asyncio

ALLOWED_GUILD_IDS = [1384950186547351552]

class BaoLoiCog(commands.Cog, name="🛠️ Báo lỗi"):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_counter = 0

    @commands.command(name="baoloi")
    async def bao_loi(self, ctx, *, content: str = None):
        if ctx.guild.id not in ALLOWED_GUILD_IDS:
            await ctx.send("🚫 Lệnh này không khả dụng trong server này.")
            return

        if not content:
            await ctx.send(
                "❗ Vui lòng nhập nội dung báo lỗi.\n"
                "📌 Cách sử dụng: `!baoloi nội dung lỗi bạn muốn báo`"
            )
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

        await channel.send(
            f"{author.mention}, cảm ơn bạn đã báo lỗi! "
            "Vui lòng nếu có thể gửi video lỗi và ghi nội dung chi tiết lỗi rõ ràng nhất có thể."
        )
        await channel.send(embed=embed)

        await ctx.send(f"✅ Đã tạo ticket báo lỗi tại kênh {channel.mention}")

        # 📨 Gửi thông báo tới user cố định
        notify_user_id = 996715877309370408
        try:
            notify_user = await self.bot.fetch_user(notify_user_id)
            await notify_user.send(
                f"🔔 Có báo lỗi mới từ **{author}**:\n"
                f"Nội dung: {content}\n"
                f"Kênh: {channel.mention}"
            )
        except discord.Forbidden:
            print(f"🚫 Không thể gửi DM cho user ID {notify_user_id}")
        except discord.NotFound:
            print(f"❌ Không tìm thấy user với ID {notify_user_id}")
        except Exception as e:
            print(f"⚠️ Lỗi khi gửi DM: {e}")

        # ⏳ Tự động xoá kênh sau 1 giờ
        await channel.send("⏳ Kênh này sẽ tự động xoá sau 1 giờ.")
        await asyncio.sleep(3600)
        try:
            await channel.delete(reason="Tự động xoá sau 1 giờ.")
        except discord.Forbidden:
            print(f"🚫 Không thể xoá kênh {channel.name}")
        except Exception as e:
            print(f"⚠️ Lỗi khi xoá kênh: {e}")

async def setup(bot):
    await bot.add_cog(BaoLoiCog(bot))
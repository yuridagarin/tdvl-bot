from discord.ext import commands, tasks
import datetime
from zoneinfo import ZoneInfo  # <-- THÊM DÒNG NÀY

class AutoNotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.scheduled_events = [
            {"hour": 10, "minute": 0, "message": "☀️ Ăn sáng nào các bằng hữu, tiệc thỏ nướng đã xuất hiện ở Thiên Ba, quý anh hùng có thể tới để tham dự tiệc"},
            {"hour": 14, "minute": 0, "message": "🍚 Đến giờ ăn trưa rồi!, tiệc thỏ nướng đã xuất hiện ở Thiên Ba, quý anh hùng có thể tới để tham dự tiệc"},
            {"hour": 22, "minute": 0, "message": "📢 Các vị anh hùng hãy cùng nhau nhăm nhi bữa tiệc tối nào, tiệc thỏ nướng đã xuất hiện ở Thiên Ba, quý anh hùng có thể tới để tham dự tiệc"},
            {"hour": 14, "minute": 55, "message": "📢 Tin sốt dẻo mới đây Boss Độc cô kim phong chỉ còn 5 phút nữa là xuất hiện ở Tây Thành Đô trên người mang theo nhiều phần quà đặc biệt mau chống tim hắn đi nào !!!"},
            {"hour": 19, "minute": 55, "message": "⚔️ Biên cương báo về chiến trường chỉ còn 5 phút nữa là đã mở, các anh hùng hảo hán hãy cùng nguyên soái tham gia để bảo vệ phe phái của mình đi nào !!!"},
        ]

        self.channel_id = 1385296312857137164  
        self.last_sent_times = set()
        self.check_time.start()

    def cog_unload(self):
        self.check_time.cancel()

    @tasks.loop(seconds=60)
    async def check_time(self):
        now = datetime.datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))  # ✅ Dùng giờ Việt Nam
        current_time = (now.hour, now.minute)

        for event in self.scheduled_events:
            key = (event["hour"], event["minute"], event["message"])

            if current_time == (event["hour"], event["minute"]):
                if key not in self.last_sent_times:
                    channel = self.bot.get_channel(self.channel_id)
                    if channel:
                        await channel.send(f"{event['message']}\n🕒 `{now.strftime('%H:%M')}`")
                    self.last_sent_times.add(key)
            else:
                self.last_sent_times.discard(key)

async def setup(bot):
    await bot.add_cog(AutoNotify(bot))
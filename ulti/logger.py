from collections import defaultdict
from datetime import datetime
import os
import re

def ghi_tong_quy_theo_ngay(nopquy_data, day=None, guild_name="default"):
    day = day or datetime.now().strftime("%Y-%m-%d")
    totals = defaultdict(int)

    # Làm sạch tên server để dùng làm tên thư mục
    guild_name = re.sub(r'[\\/*?:"<>|]', "_", guild_name)

    if day not in nopquy_data:
        print(f"⚠️ Không có dữ liệu cho ngày {day} trong server: {guild_name}")
        print("📅 Danh sách ngày:", list(nopquy_data.keys()))
        print("🕒 Ngày hiện tại hệ thống:", day)
        return

    for uid, entries in nopquy_data[day].items():
        for entry in entries:
            try:
                amount = int(entry["amount"])
                item = entry["item"]
                totals[item] += amount
            except (KeyError, ValueError, TypeError) as e:
                print(f"⚠️ Bỏ qua mục lỗi: {entry} – Lỗi: {e}")
                continue

    # Tạo thư mục logs/{guild_name}
    log_dir = os.path.join("logs", guild_name)
    os.makedirs(log_dir, exist_ok=True)

    filepath = os.path.join(log_dir, f"tong_quy_{day}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Tổng kết quỹ ngày {day} – Server: {guild_name}\n")
        for item, amount in totals.items():
            f.write(f"- {item}: {amount}\n")

    print(f"✅ Ghi log: {filepath}")

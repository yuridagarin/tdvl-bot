
from collections import defaultdict
from datetime import datetime
import os

def ghi_tong_quy_theo_ngay(nopquy_data, day=None):
    day = day or datetime.now().strftime("%Y-%m-%d")
    totals = defaultdict(int)

    # Kiểm tra ngày có trong dữ liệu không
    if day not in nopquy_data:
        print(f"⚠️ Không có dữ liệu cho ngày {day}")
        print("📅 Danh sách ngày trong nopquy_data:", list(nopquy_data.keys()))
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

    # Tạo thư mục nếu chưa có
    os.makedirs("logs", exist_ok=True)
    filepath = f"logs/tong_quy_{day}.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Tổng kết quỹ ngày {day}:\n")
        for item, amount in totals.items():
            f.write(f"- {item}: {amount}\n")

    print(f"✅ Ghi log: {filepath}")

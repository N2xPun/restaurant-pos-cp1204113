from datetime import date
import numpy as np
import matplotlib.pyplot as plt

def show_daily_revenue(record: dict[str, dict[str, np.int64]], prices: dict[str, np.int64]) -> None:
    if not record:
        print("No sales records are available.")
        return

    ordered_dates = sorted(record, key=date.fromisoformat)
    revenues = np.array([
        sum(int(quantity) * prices[item] for item, quantity in record[day].items())
        for day in ordered_dates
    ])
    date_labels = [date.fromisoformat(day).strftime("%d/%m") for day in ordered_dates]
    x_values = list(range(1, len(ordered_dates) + 1))

    plt.rcParams["font.family"] = "Tahoma"
    plt.figure(figsize=(12, 6), dpi=100)
    plt.plot(x_values, revenues, color="#1f77b4", linewidth=2.5, marker="o")
    plt.fill_between(x_values, revenues, color="#1f77b4", alpha=0.15)
    plt.title("สถิติรายได้รายวัน", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("วันที่", fontsize=12)
    plt.ylabel("รายได้ (บาท)", fontsize=12)
    plt.xticks(x_values, date_labels, rotation=30)
    plt.gca().yaxis.set_major_formatter("{x:,.0f}")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()
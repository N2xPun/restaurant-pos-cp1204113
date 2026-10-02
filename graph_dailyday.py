from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

def show_menu_sales(record: dict[str, dict[str, np.int64]], prices: dict[str, np.int64]) -> None:
    while True:
        date_text = input("Enter date to view (DD-MM-YYYY): ").strip()
        try:
            selected_date = datetime.strptime(date_text, "%d-%m-%Y").date()
            break
        except ValueError:
            print("Invalid date. Please use DD-MM-YYYY.")

    date_key = selected_date.isoformat()
    daily_sales = record.get(date_key)
    if daily_sales is None:
        print(f"No sales records found for {date_key}.")
        return

    menu_names = sorted(prices)
    quantities = [int(daily_sales.get(menu_name, 0)) for menu_name in menu_names]
    total_revenue = sum(
        quantity * prices[menu_name]
        for menu_name, quantity in zip(menu_names, quantities)
    )

    plt.rcParams["font.family"] = "Tahoma"
    figure, axis = plt.subplots(figsize=(12, 6), dpi=100)
    bars = axis.bar(
        menu_names, quantities, color="#2ca02c", edgecolor="black", alpha=0.85
    )

    for bar in bars:
        quantity = bar.get_height()
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            quantity + max(max(quantities), 1) * 0.01,
            f"{quantity} จาน",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    axis.set_title(
        f"ยอดขายแยกตามเมนู วันที่ {selected_date.strftime('%d/%m/%Y')}\n"
        f"รายได้รวม {total_revenue:,} บาท",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    axis.set_xlabel("รายการอาหาร", fontsize=12)
    axis.set_ylabel("จำนวนที่ขายได้ (จาน)", fontsize=12)
    axis.tick_params(axis="x", labelrotation=20)
    axis.grid(axis="y", linestyle="--", alpha=0.6)
    figure.tight_layout()
    plt.show()
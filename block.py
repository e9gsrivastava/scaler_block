"""
av_peak_block_prices,av_off_peak_block_prices
"""

from datetime import datetime
from csv import DictReader, DictWriter


def read_prices(file_path):
    """Reads hourly prices from a CSV file."""
    with open(file_path, "r", encoding="utf-8") as file:
        reader = DictReader(file)
        data = [
            {
                "date": datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S"),
                "price": float(entry["price"]),
            }
            for entry in reader
        ]
    return data


def calculate_blocks_and_scalars(prices_path):
    """Calculates average block prices and scalars."""
    data = read_prices(prices_path)

    grouped_data = {}
    for entry in data:
        month_key = entry["date"].strftime("%Y-%m")
        if month_key not in grouped_data:
            grouped_data[month_key] = {"peak_prices": [], "off_peak_prices": []}

        if 6 <= entry["date"].hour <= 21:
            grouped_data[month_key]["peak_prices"].append(entry["price"])
        elif 21 <= entry["date"].hour or entry["date"].hour < 6:
            grouped_data[month_key]["off_peak_prices"].append(entry["price"])

    for month_key, group in grouped_data.items():
        peak_prices = group["peak_prices"]
        if peak_prices:
            avg_peak_price = round(sum(peak_prices) / len(peak_prices), 2)
            group["avg_peak_price"] = avg_peak_price

    for month_key, group in grouped_data.items():
        off_peak_prices = group["off_peak_prices"]
        if off_peak_prices:
            avg_off_peak_price = round(sum(off_peak_prices) / len(off_peak_prices), 2)
            group["avg_off_peak_price"] = avg_off_peak_price

    return grouped_data


def write_to_csv(results, output_path):
    """Writes results to a CSV file."""
    with open(output_path, "w", newline="", encoding="utf-8") as output_file:
        writer = DictWriter(
            output_file,
            fieldnames=["date", "av_peak_block_prices", "av_off_peak_block_prices"],
        )
        writer.writeheader()
        for month_key, group in results.items():
            writer.writerow(
                {
                    "date": month_key,
                    "av_peak_block_prices": group.get("avg_peak_price", 0.0),
                    "av_off_peak_block_prices": group.get("avg_off_peak_price", 0.0),
                }
            )


if __name__ == "__main__":
    PRICESPATH = "hourly_prices.csv"
    result = calculate_blocks_and_scalars(PRICESPATH)
    OUTPUTPATH = "average_blocks.csv"
    write_to_csv(result, OUTPUTPATH)
    print(result)

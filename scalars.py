from datetime import datetime
from csv import DictReader, DictWriter

def read_hourly_prices(file_path):
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

def calculate_peak_block_by_hour(hourly_prices_path):
    data = read_hourly_prices(hourly_prices_path)

    grouped_data = {}
    days_in_month = {}

    for entry in data:
        month_key = entry["date"].strftime("%Y-%m")
        hour_key = entry["date"].hour

        if month_key not in grouped_data:
            grouped_data[month_key] = {hour: 0 for hour in range(24)}
            days_in_month[month_key] = set()

        # Consider it for the sum
        grouped_data[month_key][hour_key] += entry["price"]

        # Check if the entry is the first hour of the day
        if entry["date"].hour == 0:
            days_in_month[month_key].add(entry["date"].day)

    # Divide the sum by the number of days in each month
    for month_key in grouped_data:
        for hour in grouped_data[month_key]:
            if hour in days_in_month[month_key]:
                grouped_data[month_key][hour] /= len(days_in_month[month_key])

    return grouped_data

def write_peak_block_by_hour_to_csv(grouped_data, output_file_path):
    with open(output_file_path, "w", newline="", encoding="utf-8") as output_file:
        writer = DictWriter(output_file, fieldnames=["date", "block_value"])
        writer.writeheader()
        for month_key, month_data in grouped_data.items():
            for hour, price in month_data.items():
                row = {"date": f"{month_key}-{hour:02d}", "block_value": round(price, 2)}
                writer.writerow(row)

if __name__ == "__main__":
    hourly_prices_path = "hourly_prices.csv"

    grouped_data = calculate_peak_block_by_hour(hourly_prices_path)

    output_file_path = "peak_block_by_hour.csv"
    write_peak_block_by_hour_to_csv(grouped_data, output_file_path)

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

def calculate_energy_blocks_and_scalars(hourly_prices_path):
    data = read_hourly_prices(hourly_prices_path)

    # Group data by month and year
    grouped_data = {}
    for entry in data:
        month_year_key = entry["date"].strftime("%Y-%m")
        if month_year_key not in grouped_data:
            grouped_data[month_year_key] = {"peak_block_prices": [], "off_peak_block_prices": []}
        
        # Check if the hour is peak (6:00 to 21:00)
        if 6 <= entry["date"].hour <= 21:
            grouped_data[month_year_key]["peak_block_prices"].append(entry["price"])
        # Check if the hour is off-peak (21:00 to 00:00 or 00:00 to 6:00)
        elif 21 <= entry["date"].hour or entry["date"].hour < 6:
            grouped_data[month_year_key]["off_peak_block_prices"].append(entry["price"])

    # Calculate average peak block price for each month
    for month_year_key, group in grouped_data.items():
        peak_block_prices = group["peak_block_prices"]
        if peak_block_prices:
            avg_peak_block_price = round(sum(peak_block_prices) / len(peak_block_prices), 2)
            grouped_data[month_year_key]["avg_peak_block_price"] = avg_peak_block_price

    # Calculate average off-peak block price for each month
    for month_year_key, group in grouped_data.items():
        off_peak_block_prices = group["off_peak_block_prices"]
        if off_peak_block_prices:
            avg_off_peak_block_price = round(sum(off_peak_block_prices) / len(off_peak_block_prices), 2)
            grouped_data[month_year_key]["avg_off_peak_block_price"] = avg_off_peak_block_price

    return grouped_data

def write_to_csv(results, output_file_path):
    with open(output_file_path, "w", newline="", encoding="utf-8") as output_file:
        writer = DictWriter(output_file, fieldnames=["month_year", "avg_peak_block_price", "avg_off_peak_block_price"])
        writer.writeheader()
        for month_year_key, group in results.items():
            writer.writerow({"month_year": month_year_key, "avg_peak_block_price": group.get("avg_peak_block_price", 0.0), "avg_off_peak_block_price": group.get("avg_off_peak_block_price", 0.0)})

if __name__ == "__main__":
    hourly_prices_path = "hourly_prices.csv"
    result = calculate_energy_blocks_and_scalars(hourly_prices_path)
    
    output_file_path = "average_energy_blocks.csv"
    write_to_csv(result, output_file_path)

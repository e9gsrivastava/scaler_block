"""
Showing block_value, scalar
"""
from datetime import datetime
from csv import DictReader, DictWriter


def read_hourly_prices(file_path):
    """
    Reads hourly prices from a CSV file.
    """
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


def calculate_block_and_scalar(data):
    """
    Calculates block values and scalars for each hour
    """
    hourly_data = {}

    for entry in data:
        hour_key = entry["date"].strftime("%H:00:00")
        hourly_data.setdefault(hour_key, {"sum": 0, "count": 0})
        hourly_data[hour_key]["sum"] += entry["price"]
        hourly_data[hour_key]["count"] += 1

    block_values = {
        key: data["sum"] / data["count"] for key, data in hourly_data.items()
    }

    block_and_scalar_data = []

    for entry in data:
        hour_key = entry["date"].strftime("%H:00:00")
        block_value = block_values[hour_key]
        scalar = entry["price"] / block_value if block_value != 0 else 0

        block_and_scalar_data.append(
            {
                "date": entry["date"].strftime("%Y-%m-%d %H:00:00"),
                "block_value": round(block_value, 2),
                "scalar": round(scalar, 2),
            }
        )

    return block_and_scalar_data


def write_block_and_scalar_to_csv(data, output_file_path):
    """
    Writes block and scalar data to a CSV file.
    """
    with open(output_file_path, "w", newline="", encoding="utf-8") as output_file:
        writer = DictWriter(output_file, fieldnames=["date", "block_value", "scalar"])
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    HOURLYPATH = "hourly_prices.csv"
    dataa = read_hourly_prices(HOURLYPATH)
    block_and_scalar_dataa = calculate_block_and_scalar(dataa)

    OUTPUTPATH = "block_and_scalar_results.csv"
    write_block_and_scalar_to_csv(block_and_scalar_dataa, OUTPUTPATH)

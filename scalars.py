"""
scalar
"""
from datetime import datetime
from csv import DictReader, DictWriter


def read_hourly_prices(file_path):
    """
    Read the csv file
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


def calculate_hourly_data(month_data):
    """
    Calculate sum and count for each hour in a month
    """
    hourly_data = {}

    for entry in month_data:
        hour_key = entry["date"].strftime("%H:00:00")
        hourly_data.setdefault(hour_key, {"sum": 0, "count": 0})
        hourly_data[hour_key]["sum"] += entry["price"]
        hourly_data[hour_key]["count"] += 1

    return hourly_data


def calculate_block_values(hourly_data, peak_threshold, off_peak_threshold):
    """
    Calculate peak and off-peak block values for a month
    """
    block_values = {
        key: data["sum"] / data["count"] for key, data in hourly_data.items()
    }

    peak_hour_keys = [
        key
        for key in block_values
        if peak_threshold[0] <= int(key[:2]) <= peak_threshold[1]
    ]
    off_peak_hour_keys = [
        key
        for key in block_values
        if int(key[:2]) < off_peak_threshold[0] or int(key[:2]) >= off_peak_threshold[1]
    ]

    peak_block_value = (
        round(
            sum(block_values[key] for key in peak_hour_keys) / len(peak_hour_keys),
            2,
        )
        if peak_hour_keys
        else 0
    )
    off_peak_block_value = (
        round(
            sum(block_values[key] for key in off_peak_hour_keys)
            / len(off_peak_hour_keys),
            2,
        )
        if off_peak_hour_keys
        else 0
    )

    return peak_block_value, off_peak_block_value, peak_hour_keys, off_peak_hour_keys


def calculate_block_and_scalar(data):
    """
    Calculate block and scalar
    """
    monthly_data = {month: [] for month in range(1, 13)}

    for entry in data:
        month = entry["date"].month
        monthly_data[month].append(entry)

    block_and_scalar_data = []

    for month, month_data in monthly_data.items():
        hourly_data = calculate_hourly_data(month_data)

        (
            peak_block_value,
            off_peak_block_value,
            peak_hour_keys,
            off_peak_hour_keys,
        ) = calculate_block_values(
            hourly_data, peak_threshold=(6, 21), off_peak_threshold=(6, 22)
        )

        for entry in month_data:
            hour_key = entry["date"].strftime("%H:00:00")
            block_value = hourly_data[hour_key]["sum"] / hourly_data[hour_key]["count"]
            new_scalar = (
                block_value / peak_block_value
                if hour_key in peak_hour_keys
                else block_value / off_peak_block_value
                if hour_key in off_peak_hour_keys
                else 0
            )

            block_and_scalar_data.append(
                {
                    "date": entry["date"].strftime("%Y-%m-%d %H:00:00"),
                    "month": month,
                    "av_price": round(block_value, 2),
                    "block_type": "Peak" if hour_key in peak_hour_keys else "Off-Peak",
                    "block_value": peak_block_value
                    if hour_key in peak_hour_keys
                    else off_peak_block_value,
                    "scalar": round(new_scalar, 2),
                }
            )

    return block_and_scalar_data


def write_block_and_scalar_to_csv(data, output_file_path):
    """
    Write the result to a csv file
    """
    with open(output_file_path, "w", newline="", encoding="utf-8") as output_file:
        writer = DictWriter(
            output_file,
            fieldnames=[
                "date",
                "month",
                "av_price",
                "block_type",
                "block_value",
                "scalar",
            ],
        )
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    HOURLY_PATH = "hourly_prices.csv"
    OUTPUT_PATH = "block_and_scalar_results.csv"

    dataa = read_hourly_prices(HOURLY_PATH)
    block_and_scalar_dataa = calculate_block_and_scalar(dataa)
    write_block_and_scalar_to_csv(block_and_scalar_dataa, OUTPUT_PATH)

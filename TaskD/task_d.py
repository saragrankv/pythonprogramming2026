# Copyright © 2026 Sara Grankvist

"""
A program that reads electricity consumption and production
data from a CSV file, calculates daily totals and prints it 
to the console in a user-friendly table.
"""

from datetime import datetime, date

WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

# Using constant to not have to type 1000 every time when converting Wh to kWh 
K = 1000.00

def convert_data(raw_data: list) -> list:
    """
    Converts data to the correct data types:
    Time stamp: datetime
    Phase data: float, divided by 1000 to get value in kWh instead of Wh

    Parameters:
     raw_data (list): list where every field is in str format

    Returns:
     converted_data (list): list with fields in correct data types 
    """
    converted_data = []
    # Convert the timestamp to datetime
    timestamp_dt = datetime.strptime(raw_data[0], "%Y-%m-%dT%H:%M:%S")
    converted_data.append(timestamp_dt)
    # Convert consumption and production phases to float and Wh to kWh
    cons_p1 = float(raw_data[1])/K
    converted_data.append(cons_p1)
    cons_p2 = float(raw_data[2])/K
    converted_data.append(cons_p2)
    cons_p3 = float(raw_data[3])/K
    converted_data.append(cons_p3)
    prod_p1 = float(raw_data[4])/K
    converted_data.append(prod_p1)
    prod_p2 = float(raw_data[5])/K
    converted_data.append(prod_p2)
    prod_p3 = float(raw_data[6])/K
    converted_data.append(prod_p3)
    return converted_data

def read_data(filename: str) -> list[list]:
    """
    Reads the CSV data and returns rows converted to correct data
    types in a list

    Parameters:
     filename (str): Name of the CSV file

    Returns:
     converted_data (list[list]): Read and converted data
    """
    data_rows = []
    converted_data = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            fields = line.split(";")
            data_rows.append(fields)
    # Slice the first (heading) row off the list and call function to
    # convert it to correct data types:
    for row in data_rows[1:]:
        converted_data.append(convert_data(row))
    return converted_data

def calculate_daily_totals(data_list: list[list]) -> list[list]:
    """
    Calculate consumption and production totals per day and sort
    them into a list per day and phase. Designed to work regardless
    of how many days of data is in the CSV file.

    Parameters:
     data_list (list[list]): list of lists, hourly consumption and 
     production per phase

    Returns:
     days_list (list[list]): daily total consumption and production
     per phase
    """
    days_list = []
    current_day = None
    daycount = -1
    for row in data_list:
        if isinstance(row[0], datetime):
            if current_day is None or current_day != row[0].date():
                current_day = row[0].date()
                day = [current_day, row[1], row[2], row[3], row[4], row[5], row[6]]
                daycount += 1
                days_list.append(day)
            else:
                # add to daily total per phase
                for i in range(1, 7):
                    days_list[daycount][i] += row[i]
    return days_list

def print_daily_totals (daily_totals: list) -> None:
    print("Week 42 electricity consumption and production (kWh, by phase)")
    print("\nDay           Date           Consumption [kWh]              Production [kWh]")
    print("            (dd.mm.yyyy)    v1       v2      v3            v1      v2      v3")
    print("------------------------------------------------------------------------------")
    for row in daily_totals:
        date = row[0]
        weekday = date.weekday()
        formatted_date = date.strftime("%d.%m.%Y")
        cons_p1 = f"{row[1]:.2f}".replace(".",",")
        cons_p2 = f"{row[2]:.2f}".replace(".",",")
        cons_p3 = f"{row[3]:.2f}".replace(".",",")
        prod_p1 = f"{row[4]:.2f}".replace(".",",")
        prod_p2 = f"{row[5]:.2f}".replace(".",",")
        prod_p3 = f"{row[6]:.2f}".replace(".",",")
        # Align the columns for each row so that the output is easily readable
        print(f"{WEEKDAYS[weekday]:<12}{formatted_date:<12}{cons_p1:>8}{cons_p2:>8}{cons_p3:>8}{prod_p1:>14}{prod_p2:>8}{prod_p3:>8}")

def main() -> None:
    """
    Main function: read data, compute daily totals, print report
    """
    # Read data from the file and store the data in a list
    data_list = read_data("week42.csv")
    daily_totals = calculate_daily_totals(data_list)
    print_daily_totals(daily_totals)
        
if __name__ == "__main__":
    main()
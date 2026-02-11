# Copyright © 2026 Sara Grankvist
# License: MIT

"""
A program that reads electricity consumption and production
data from CSV files, calculates daily totals and saves a 
summary into a file in a user-friendly way.
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

def write_summaries (daily_totals: list, week_number: int, filename: str) -> None:
    """
    Create a weekly summary based on the daily totals, a summary for the entire period,
    and write it to a file
    
    Parameters:
     daily_totals (list): list of daily totals calculated for the period
     week_number (int): the number of the first week in the data
     filename (str): the name of the file the summary is written to
    """
    weekly_summary = ""
    total_cons_p1 = 0.0
    total_cons_p2 = 0.0
    total_cons_p3 = 0.0
    total_prod_p1 = 0.0
    total_prod_p2 = 0.0
    total_prod_p3 = 0.0
    for row in daily_totals:
        date = row[0]
        weekday = date.weekday()
        formatted_date = date.strftime("%d.%m.%Y")
        # Read the consumption and production per phase from the list
        cons_p1 = row[1]
        cons_p2 = row[2]
        cons_p3 = row[3]
        prod_p1 = row[4]
        prod_p2 = row[5]
        prod_p3 = row[6]
        # Format the consumption and production per phase according to task
        str_cons_p1 = f"{cons_p1:.2f}".replace(".",",")
        str_cons_p2 = f"{cons_p2:.2f}".replace(".",",")
        str_cons_p3 = f"{cons_p3:.2f}".replace(".",",")
        str_prod_p1 = f"{prod_p1:.2f}".replace(".",",")
        str_prod_p2 = f"{prod_p2:.2f}".replace(".",",")
        str_prod_p3 = f"{prod_p3:.2f}".replace(".",",")
        # Add consumption and production per phase to totals
        total_cons_p1 += cons_p1
        total_cons_p2 += cons_p2
        total_cons_p3 += cons_p3
        total_prod_p1 += prod_p1
        total_prod_p2 += prod_p2
        total_cons_p3 += prod_p3
        # Add header rows and increase the week number for each before each Monday and increase the week count for each Monday:
        if weekday == 0:
                # Add empty line at the beginning if the string isn't empty:
                if weekly_summary != "":
                    weekly_summary += "\n\n" 
                weekly_summary += f"Week {str(week_number)} electricity consumption and production (kWh, by phase)"
                weekly_summary += ("\nDay           Date           Consumption [kWh]              Production [kWh]")
                weekly_summary += ("\n            (dd.mm.yyyy)    v1       v2      v3            v1      v2      v3")
                weekly_summary += ("\n------------------------------------------------------------------------------")
                week_number += 1
        # Align the columns for each row so that the output is easily readable
        weekly_summary += (f"\n{WEEKDAYS[weekday]:<12}{formatted_date:<12}{str_cons_p1:>8}{str_cons_p2:>8}{str_cons_p3:>8}{str_prod_p1:>14}{str_prod_p2:>8}{str_prod_p3:>8}")
    # At the end, add totals for the entire period
    total_str_cons_p1 = f"{total_cons_p1:.2f}".replace(".",",")
    total_str_cons_p2 = f"{total_cons_p2:.2f}".replace(".",",")
    total_str_cons_p3 = f"{total_cons_p3:.2f}".replace(".",",")
    total_str_prod_p1 = f"{total_prod_p1:.2f}".replace(".",",")
    total_str_prod_p2 = f"{total_prod_p2:.2f}".replace(".",",")
    total_str_prod_p3 = f"{total_prod_p3:.2f}".replace(".",",")
    weekly_summary += "\n\nSummary of the entire period by phase:"
    weekly_summary += ("\n   Consumption [kWh]              Production [kWh]")
    weekly_summary += ("\n  v1       v2      v3            v1      v2      v3")
    weekly_summary += ("\n----------------------------------------------------")
    weekly_summary += (f"\n{total_str_cons_p1}{total_str_cons_p2:>8}{total_str_cons_p3:>8}{total_str_prod_p1:>14}{total_str_prod_p2:>8}{total_str_prod_p3:>8}\n")
    # Write data to file
    try:
        # Create the file if it doesn't exist
        with open(filename, "x", encoding="utf-8") as f:
            f.write(weekly_summary)
            print(f"{filename} created")
    except FileExistsError:
        # Append the contents of the file if it already exists, separate new output from previous
        with open(filename, "a", encoding="utf-8") as f:
            f.write("\n--- (new report begins here) ---\n\n" + weekly_summary)
            print(f"{filename} appended")


def main() -> None:
    """
    Main function: read data, compute daily totals, print report
    """
    # Read data from the file and store the data in a list
    data_list = read_data("week41.csv")
    # Read data from the second file and add it to the same list as the first week
    data_week42 = read_data("week42.csv")
    for item in data_week42:
        data_list.append(item)
    # Do the same for the third file
    data_week43 = read_data("week43.csv")
    for item in data_week43:
        data_list.append(item)
    daily_totals = calculate_daily_totals(data_list)
    write_summaries(daily_totals, 41, "summary.txt")
        
if __name__ == "__main__":
    main()
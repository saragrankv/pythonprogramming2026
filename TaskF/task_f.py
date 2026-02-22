# Copyright © 2026 Sara Grankvist
# License: MIT

"""
A program that reads a CSV file containing a year's worth of data of electricity
consumption and production, and creates monthly and yearly summaries or a summary
of a custom time period, which it can write into a file.
"""

from datetime import datetime, date

IN_FILE = "2025.csv"
OUT_FILE = "summary.txt"
MONTHS = [
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

def convert_data(data_row: list) -> dict:
    """
    Converts a row of data read from the CSV file to the correct
    datatypes.

    Parameters:
     data_row (list): a row of data from the CSV file split into a list
    Returns:
     row_dict (dict): a dictionary of the data with descriptive keys and
                      the correct datatypes
    """
    row_dict = {}
    # Convert the timestamp to datetime
    row_dict["timestamp"] = datetime.fromisoformat(data_row[0])
    row_dict["consumption"] = float(data_row[1].replace(",", "."))
    row_dict["production"] = float(data_row[2].replace(",", "."))
    row_dict["average_temp"] = float(data_row[3].replace(",", "."))
    return row_dict

def read_data() -> list:
    """
    Reads the data from the CSV file (hardcoded), splits it into a list,
    calls the function to convert each row into a dict with the correct 
    data types and adds the dicts into a list which it returns

    Returns:
     converted_data (list): a list of dictionaries with the data converted
                            into the correct datatypes
    """
    unconverted_data = []
    converted_data = []
    with open(IN_FILE, "r", encoding="utf-8") as f:
        for line in f:
            fields = line.split(";")
            unconverted_data.append(fields)
    # Skip the header row of the file and convert the data into
    # a list of dictionaries with the right data types
    for row in unconverted_data[1:]:
        converted_data.append(convert_data(row))
    return converted_data

def write_data_to_file(data_str: str) -> None:
    """
    Writes a report into a text file

    Parameters:
     data_str (str): The the consumption/production report as a string
    """
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(data_str)
        print(f"- - -\nReport written to {OUT_FILE}\n- - -")


def daily_summary(startdate: date, enddate: date, data_list: list) -> str:
    """
    Returns a formatted summary of energy consumption and production for
    the given period.

    Parameters:
     startdate (date): the start date given by the user
     enddate (date): the end date given by the user
     data_list (list): the data in a list of dictionaries with the correct datatypes
    """
    total_cons = 0.0
    total_prod = 0.0
    temp_sum = 0.0
    day_count = 0
    summary = ""
    for row in data_list:
        if row["timestamp"].date() >= startdate and row["timestamp"].date() <= enddate:
            total_cons += row["consumption"]
            total_prod += row["production"]
            if row["timestamp"].hour == 0 and row["timestamp"].minute == 0:
                temp_sum += row["average_temp"]
                day_count += 1
    # Calculate average temperature for the entire period
    avg_temp = temp_sum / day_count
    summary += f"Report for the period {startdate.strftime("%d.%m.%Y")}-{enddate.strftime("%d.%m.%Y")}\n"
    summary += f"- Total consumption: {total_cons:.2f} kWh\n".replace(".", ",")
    summary += f"- Total production: {total_prod:.2f} kWh\n".replace(".", ",")
    summary += f"- Average temperature: {avg_temp:.2f} °C\n".replace(".", ",")
    return summary

def monthly_summary(month: int, data_list: list) -> str:
    """
    Returns a formatted summary of consumption and production
    for a given month

    Parameters:
     month (int): the month number given by the user
     data_list (list): the data converted into a list of dictionaries with correct data types
    Returns:
     summary (str): Summary of the month formatted as a string
    """
    total_cons = 0.0
    total_prod = 0.0
    temp_sum = 0.0
    day_count = 0
    summary = ""
    for row in data_list:
        if row["timestamp"].date().month == month:
            total_cons += row["consumption"]
            total_prod += row["production"]
            if row["timestamp"].hour == 0 and row["timestamp"].minute == 0:
                temp_sum += row["average_temp"]
                day_count += 1
    # Calculate average temperature for the entire period
    avg_temp = temp_sum / day_count
    summary += f"Report for the month: {MONTHS[month]}\n"
    summary += f"- Total consumption: {total_cons:.2f} kWh\n".replace(".", ",")
    summary += f"- Total production: {total_prod:.2f} kWh\n".replace(".", ",")
    summary += f"- Average temperature: {avg_temp:.2f} °C\n".replace(".", ",")
    return summary

def yearly_summary(data_list: list) -> str:
    """
    Returns a formatted summary of consumption and production
    for the entire year

    Parameters:
     data_list (list): the data converted into a list of dictionaries with correct data types
    Returns:
     summary (str): Summary of the year formatted as a string
    """
    total_cons = 0.0
    total_prod = 0.0
    temp_sum = 0.0
    day_count = 0
    summary = ""
    year = data_list[0]["timestamp"].date().year
    for row in data_list:
        total_cons += row["consumption"]
        total_prod += row["production"]
        if row["timestamp"].hour == 0 and row["timestamp"].minute == 0:
            temp_sum += row["average_temp"]
            day_count += 1
    # Calculate average temperature for the entire period
    avg_temp = temp_sum / day_count
    summary += f"Report for the year: {year}\n"
    summary += f"- Total consumption: {total_cons:.2f} kWh\n".replace(".", ",")
    summary += f"- Total production: {total_prod:.2f} kWh\n".replace(".", ",")
    summary += f"- Average temperature: {avg_temp:.2f} °C\n".replace(".", ",")
    return summary


def daily_summary_menu() -> bool:
    """
    Handles the menu for printing the daily summary. Asks the user for start and end
    dates for the period to be summarized, checks that they are in the correct format,
    calls the daily summary function, prints the report and asks if the user wants to
    save it to a file. Returns a boolean to tell the main menu function if the user
    wants to keep running the program or exit it.

    Returns:
     exit (bool): Tells the main menu function whether to exit the program or not.
    """
    exit = False
    startdate = None
    enddate = None
    # Ask user for start date
    while True:
        sd_in = input("Enter start date (DD.MM.YYYY): ")
        try:
            startdate = datetime.strptime(sd_in, "%d.%m.%Y").date()
            if startdate.year == 2025:
                break
            else:
                print("Please enter a date in the year 2025")

        except ValueError:
            continue
    # Ask user for end date
    while True:
        ed_in = input("Enter end date (DD.MM.YYYY): ")
        try:
            enddate = datetime.strptime(ed_in, "%d.%m.%Y").date()
            if enddate.year == 2025:
                break
            else:
                print("Please enter a date in the year 2025")
            break
        except ValueError:
            continue
    data_list = read_data()
    report = daily_summary(startdate, enddate, data_list)
    print("\n-----------------------------------------------------")
    print(report)
    while True:
        print("What would you like to do next?")
        print("1) Write the report to the file report.txt")
        print("2) Create a new report")
        print("3) Exit")
        choice = input("Please type your choice (1-3) and press Enter: ")
        if choice.isdigit():
            match int(choice):
                case 1:
                    write_data_to_file(report)
                    continue
                case 2:
                    # Exit to the main menu but tell the program
                    # to keep running 
                    return exit
                case 3:
                    # Exit to the main menu and tell the program to
                    # terminate
                    exit = True
                    return exit
                case _:
                    continue

def monthly_summary_menu() -> bool:
    """
    Handles the menu for printing the monthly summary. Asks the user for the month number,
    calls the monthly summary function, prints the report and asks if the user wants to
    save it to a file. Returns a boolean to tell the main menu function if the user
    wants to keep running the program or exit it.

    Returns:
     exit (bool): Tells the main menu function whether to exit the program or not.
    """
    exit = False
    # Ask user for month:
    while True:
        month = input("Enter month number (1-12): ").strip()
        if month.isdigit() and int(month) in range(1, 13):
            break
    data_list = read_data()
    report = monthly_summary(int(month), data_list)
    print("\n-----------------------------------------------------")
    print(report)
    while True:
        print("What would you like to do next?")
        print("1) Write the report to the file report.txt")
        print("2) Create a new report")
        print("3) Exit")
        choice = input("Please type your choice (1-3) and press Enter: ")
        if choice.isdigit():
            match int(choice):
                case 1:
                    write_data_to_file(report)
                    continue
                case 2:
                    # Exit to the main menu but tell the program
                    # to keep running 
                    return exit
                case 3:
                    # Exit to the main menu and tell the program to
                    # terminate
                    exit = True
                    return exit
                case _:
                    continue

def yearly_summary_menu() -> bool:
    """
    Handles the menu for printing the yearly summary. Calls the yearly summary function, 
    prints the report and asks if the user wants to save it to a file. Returns a boolean 
    to tell the main menu function if the user wants to keep running the program or exit it.

    Returns:
     exit (bool): Tells the main menu function whether to exit the program or not.
    """
    exit = False
    data_list = read_data()
    report = yearly_summary(data_list)
    print("\n-----------------------------------------------------")
    print(report)
    while True:
        print("What would you like to do next?")
        print("1) Write the report to the file report.txt")
        print("2) Create a new report")
        print("3) Exit")
        choice = input("Please type your choice (1-3) and press Enter: ")
        if choice.isdigit():
            match int(choice):
                case 1:
                    write_data_to_file(report)
                    continue
                case 2:
                    # Exit to the main menu but tell the program
                    # to keep running 
                    return exit
                case 3:
                    # Exit to the main menu and tell the program to
                    # terminate
                    exit = True
                    return exit
                case _:
                    continue


def mainmenu() -> None:
    """
    Main menu function. Calls submenu functions depending on the user's
    choice and depending on what they return, keeps runnning or exits.
    """
    while True:
        print("Choose a report type:")
        print("1) Daily summary for a date range")
        print("2) Monthly summary for one month")
        print("3) Full year 2025 summary")
        print("4) Exit the program")
        choice = input("Please type your choice (1-4) and press Enter: ")
        if choice.isdigit():
            match int(choice):
                case 1:
                    exit = daily_summary_menu()
                    if exit: break
                case 2:
                    exit = monthly_summary_menu()
                    if exit: break
                case 3:
                    exit = yearly_summary_menu()
                    if exit: break
                case 4:
                    break
                case _:
                    continue

def main() -> None:
    """
    Main function: calls the main menu function
    """
    mainmenu()
        
if __name__ == "__main__":
    main()
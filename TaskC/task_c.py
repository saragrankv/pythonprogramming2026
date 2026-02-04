# Copyright (c) 2026 Ville Heikkiniemi, Luka Hietala, Luukas Kola
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by Sara Grankvist according to given task

"""
A program that prints reservation information according to task requirements

The data structure and example data record:

reservationId | name | email | phone | reservationDate | reservationTime | durationHours | price | confirmed | reservedResource | createdAt
------------------------------------------------------------------------
201 | Moomin Valley | moomin@whitevalley.org | 0509876543 | 2025-11-12 | 09:00:00 | 2 | 18.50 | True | Forest Area 1 | 2025-08-12 14:33:20
int | str | str | str | date | time | int | float | bool | str | datetime

"""

from datetime import datetime, date, time

HEADERS = [
    "reservationId",
    "name",
    "email",
    "phone",
    "reservationDate",
    "reservationTime",
    "durationHours",
    "price",
    "confirmed",
    "reservedResource",
    "createdAt",
]

def convert_reservation_data(reservation: list) -> list:
    """
    Convert data types to meet program requirements

    Parameters:
     reservation (list): Unconverted reservation -> 11 columns

    Returns:
     converted (list): Converted data types
    """
    converted = []
    # Convert the first element = reservation[0]
    converted.append(int(reservation[0]))  # reservationId (str -> int)
    # And continue from here
    # No need to convert strings for the next 3
    converted.append(reservation[1])  # name (str)
    converted.append(reservation[2])  # email (str)
    converted.append(reservation[3])  # phone (str)
    reservation_date = datetime.strptime(reservation[4], "%Y-%m-%d").date()
    converted.append(reservation_date)  # reservationDate (date)
    reservation_time = datetime.strptime(reservation[5], "%H:%M").time()
    converted.append(reservation_time)  # reservationTime (time)
    converted.append(int(reservation[6]))  # durationHours (int)
    converted.append(float(reservation[7]))  # price (float)
    confirmed = True if reservation[8] == "True" else False
    converted.append(confirmed)  # confirmed (bool)
    converted.append(reservation[9])  # reservedResource (str)
    # Calling strip() to remove newline character at the end of the line
    created_at = datetime.strptime(reservation[10].strip(), "%Y-%m-%d %H:%M:%S")
    converted.append(created_at)  # createdAt (datetime)
    return converted

def fetch_reservations(reservation_file: str) -> list:
    """
    Reads reservations from a file and returns the reservations converted
    You don't need to modify this function!

    Parameters:
     reservation_file (str): Name of the file containing the reservations

    Returns:
     reservations (list): Read and converted reservations
    """
    reservations = []
    with open(reservation_file, "r", encoding="utf-8") as f:
        for line in f:
            fields = line.split("|")
            reservations.append(convert_reservation_data(fields))
    return reservations

def confirmed_reservations(reservations: list[list]) -> None:
    """
    Print confirmed reservations

    Parameters:
     reservations (list): Reservations
    """
    for reservation in reservations:
        # Check if the reservation is confirmed
        confirmed = reservation[8]
        if confirmed:
            name = reservation[1]
            resource = reservation[9]
            date = reservation[4]
            date = date.strftime("%d.%m.%Y")
            time = reservation[5]
            time = time.strftime("%H.%M")
            print(f"- {name}, {resource}, {date} at {time}")

def long_reservations(reservations: list[list]) -> None:
    """
    Print long reservations

    Parameters:
     reservations (list): Reservations
    """
    for reservation in reservations:
        # Check duration
        duration = reservation[6]
        if duration >= 3:
            name = reservation[1]
            date = reservation[4]
            date = date.strftime("%d.%m.%Y")
            time = reservation[5]
            time = time.strftime("%H.%M")
            duration = str(duration)
            resource = reservation[9]
            print(f"- {name}, {date} at {time}, duration {duration} h, {resource}")

def confirmation_statuses(reservations: list[list]) -> None:
    """
    Print confirmation statuses

    Parameters:
     reservations (list): Reservations
    """
    for reservation in reservations:
        name = reservation[1]
        confirmed = "Confirmed" if reservation[8] else "NOT Confirmed"
        print(f"{name} → {confirmed}")

def confirmation_summary(reservations: list[list]) -> None:
    """
    Print confirmation summary

    Parameters:
     reservations (list): Reservations
    """
    confirmed_count = 0
    not_confirmed_count = 0
    for reservation in reservations:
        if reservation[8]: 
            confirmed_count += 1 
        else:
            not_confirmed_count += 1
    print(f"- Confirmed reservations: {str(confirmed_count)} pcs")
    print(f"- Not confirmed reservations: {str(not_confirmed_count)} pcs")

def total_revenue(reservations: list[list]) -> None:
    """
    Print total revenue

    Parameters:
     reservations (list): Reservations
    """
    revenue = 0
    for reservation in reservations:
        price = reservation[7]
        confirmed = reservation[8]
        if confirmed:
            revenue += price
    revenue_str = f"{revenue:.2f}".replace(".",",")
    print(f"Total revenue from confirmed reservations: {revenue_str} €")

def main():
    """
    Prints reservation information according to requirements
    Reservation-specific printing is done in functions
    """
    reservations = fetch_reservations("reservations.txt")
    # PART A -> Before continuing to part B, make sure that the following lines
    # print all the reservation data and the correct data types to the console. 
    # After that, you can remove this section or comment it out up to part B.
    # print(" | ".join(HEADERS))
    # print("------------------------------------------------------------------------")
    # for reservation in reservations:
    #    print(" | ".join(str(x) for x in reservation))
    #    data_types = [type(x).__name__ for x in reservation]
    #    print(" | ".join(data_types))
    #    print(
    #        "------------------------------------------------------------------------"
    #    )

    # PART B -> Build the output required in part B from this using
    # the predefined functions and the necessary print statements.

    print("1) Confirmed Reservations")
    confirmed_reservations(reservations)
    # Continue from here
    print("\n2) Long Reservations (≥ 3 h)")
    long_reservations(reservations)
    print("\n3) Reservation Confirmation Status")
    confirmation_statuses(reservations)
    print("\n4) Confirmation Summary")
    confirmation_summary(reservations)
    print("\n5) Total Revenue from Confirmed Reservations")
    total_revenue(reservations)

if __name__ == "__main__":
    main()

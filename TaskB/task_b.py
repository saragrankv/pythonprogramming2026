# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by Sara Grankvist according to given task

"""
A program that reads reservation data from a file
and prints them to the console using functions:

Reservation number: 123
Booker: Anna Virtanen
Date: 31.10.2025
Start time: 10.00
Number of hours: 2
Hourly rate: 19,95 €
Total price: 39,90 €
Paid: Yes
Venue: Meeting Room A
Phone: 0401234567
Email: anna.virtanen@example.com

"""
from datetime import datetime

def print_reservation_number(reservation: list) -> None:
    """
    Prints the reservation number

    Parameters:
     reservation (lst): reservation -> columns separated by |
    """
    # This type conversion isn't strictly necessary (input and 
    # output are both strings) but I'm assuming the variable data 
    # types should be converted to the ones given in the task:
    reservation_number = int(reservation[0])
    print(f"Reservation number: {str(reservation_number)}")

def print_booker(reservation: list) -> None:
    """
    Prints the booker name (Docstring changed based on function name /SG)

    Parameters:
     reservation (lst): reservation -> columns separated by |
    """
    booker = reservation[1]
    print(f"Booker: {booker}")

def print_date(reservation: list) -> None:
    """
    Prints the reservation date

    Parameters:
     reservation (lst): reservation -> columns separated by |
    """
    date = datetime.strptime(reservation[2], "%Y-%m-%d").date()
    # Convert to Finnish date format:
    date = date.strftime("%d.%m.%Y")
    print(f"Date: {date}")

def print_start_time(reservation: list) -> None:
    """
    Prints the reservation start time

    Parameters:
     reservation (lst): reservation -> columns separated by |
    """
    start_time = datetime.strptime(reservation[3], "%H:%M").time()
    # Convert to Finnish time format:
    start_time = start_time.strftime("%H.%M")
    print(f"Start time: {start_time}")

def print_hours(reservation: list) -> None:
    """
    Prints the number of hours

    Parameters:
     reservation (lst): reservation -> columns separated by |
    """
    # Again, not strictly necessary type conversion
    hours = int(reservation[4])
    print(f"Number of hours: {str(hours)}")

def print_hourly_rate(reservation: list) -> None:
    """
    Prints the hourly rate

    Parameters:
     reservation (lst): reservation -> columns separated by |
    """
    # Could simply change the decimal separator in the string
    # to a comma, but converting to float here and making sure
    # it is printed with 2 decimal places:
    hourly_rate = float(reservation[5])
    hourly_rate= f"{hourly_rate:.2f}".replace('.', ',')
    print(f"Hourly rate: {hourly_rate} €")

def print_total_price(reservation: list) -> None:
    """
    Calculates total price pased on number of hours 
    and hourly rate and prints it

    Parameters:
     reservation (lst): reservation -> columns separated by |
    """
    hours = int(reservation[4])
    hourly_rate = float(reservation[5])
    total_price = hours * hourly_rate
    # Convert to string in Finnish format:
    total_price = f"{total_price:.2f}".replace('.', ',')
    print(f"Total price: {total_price} €")

def print_paid(reservation: list) -> None:
    """
    Prints whether the reservation is paid or not

    Parameters:
     reservation (lst): reservation -> columns separated by |
    """
    paid = bool(reservation[6])
    print(f"Paid: {'Yes' if paid else 'No'}")

def print_venue(reservation: list) -> None:
    """
    Prints the name of the booked resource

    Parameters:
     reservation (lst): reservation -> columns separated by |
    """
    venue = reservation[7]
    print(f"Location: {venue}")

def print_phone(reservation: list) -> None:
    """
    Prints the booker's phone number

    Parameters:
     reservation (lst): reservation -> columns separated by |
    """
    phone = reservation[8]
    print(f"Phone: {phone}")

def print_email(reservation: list) -> None:
    """
    Prints the booker's email address

    Parameters:
     reservation (lst): reservation -> columns separated by |
    """
    email = reservation[9]
    print(f"Email: {email}")

def main():
    """
    Reads reservation data from a file and
    prints them to the console using functions
    """
    # Define the file name directly in the code
    reservations = "reservations.txt"

    # Open the file, read it, and split the contents
    with open(reservations, "r", encoding="utf-8") as f:
        reservation = f.read().strip()
        reservation = reservation.split('|')

    # Implement the remaining parts following
    # the function print_booker(reservation)
    
    # The functions to be created should perform type conversions
    # and print according to the sample output

    print_reservation_number(reservation)
    print_booker(reservation)
    print_date(reservation)
    print_start_time(reservation)
    print_hours(reservation)
    print_hourly_rate(reservation)
    print_total_price(reservation)
    print_paid(reservation)
    print_venue(reservation)
    print_phone(reservation)
    print_email(reservation)

if __name__ == "__main__":
    main()
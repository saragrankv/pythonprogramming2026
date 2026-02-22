# Copyright (c) 2026 Ville Heikkiniemi, Luka Hietala, Luukas Kola
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by Sara Grankvist according to given task

"""
A program that prints reservation information according to requirements

The data structure and example data record:

reservationId | name | email | phone | reservationDate | reservationTime | durationHours | price | confirmed | reservedResource | createdAt
------------------------------------------------------------------------
201 | Moomin Valley | moomin@whitevalley.org | 0509876543 | 2025-11-12 | 09:00:00 | 2 | 18.50 | True | Forest Area 1 | 2025-08-12 14:33:20
int | str | str | str | date | time | int | float | bool | str | datetime

"""

from datetime import datetime, date, time

class Reservation:
    def __init__(self, reservation_id: int, name: str, email: str, phone: str, date: date, 
                 time: time, duration: int, price: float, confirmed: bool, resource: str, created: datetime):
        self.reservation_id = reservation_id
        self.name = name
        self.email = email
        self.phone = phone
        self.date = date
        self.time = time
        self.duration = duration
        self.price = price
        self.confirmed = confirmed
        self.resource = resource
        self.created = created

    def is_confirmed(self):
        return self.confirmed
    
    def is_long(self):
        return self.duration >= 3
    
    def total_price(self):
        return self.duration * self.price

def convert_reservation_data(reservation: list) -> Reservation:
    """
    Convert data types to meet program requirements

    Parameters:
     reservation (list): Unconverted reservation -> 11 columns 

    Returns:
     converted (Reservation): the reservation as a Reservation object, with correct data types as attributes
    """

    reservation_id = int(reservation[0])  # reservationId (str -> int)
    name = str(reservation[1])  # name (str)
    email = str(reservation[2])  # email (str)
    phone = str(reservation[3])  # phone (str)
    date = datetime.strptime(reservation[4], "%Y-%m-%d").date()  # reservationDate (date)
    time = datetime.strptime(reservation[5], "%H:%M").time()  # reservationTime (time)
    duration = int(reservation[6])  # durationHours (int)
    price = float(reservation[7])  # price (float)
    confirmed = True if reservation[8].strip() == 'True' else False  # confirmed (bool)
    resource = str(reservation[9])  # reservedResource (str)
    created = datetime.strptime(str(reservation[10]).strip(), "%Y-%m-%d %H:%M:%S")  # createdAt (datetime)
    converted = Reservation(reservation_id, name, email, phone, date, time, duration, price, confirmed, resource, created)
    return converted


def fetch_reservations(reservation_file: str) -> list[Reservation]:
    """
    Reads reservations from a file and returns the reservations converted
    You don't need to modify this function!

    Parameters:
     reservation_file (str): Name of the file containing the reservations

    Returns:
     reservations (list): Read and converted reservations
    """
    reservations = []
    reservations.append(
        [
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
    )
    with open(reservation_file, "r", encoding="utf-8") as f:
        for line in f:
            if len(line) > 1:
                fields = line.split("|")
                reservations.append(convert_reservation_data(fields))
    return reservations

def confirmed_reservations(reservations: list[Reservation]) -> None:
    """
    Print confirmed reservations

    Parameters:
     reservations (list): Reservations
    """
    for reservation in reservations[1:]:
        if reservation.is_confirmed(): # If confirmed
            print(f'- {reservation.name}, {reservation.resource}, {reservation.date.strftime("%d.%m.%Y")} at {reservation.time.strftime("%H.%M")}')

def long_reservations(reservations : list[Reservation]) -> None:
    """
    Print long reservations

    Parameters:
     reservations (list): Reservations
    """
    for reservation in reservations[1:]:
        if reservation.is_long(): # If long
            print(f'- {reservation.name}, {reservation.date.strftime("%d.%m.%Y")} at {reservation.time.strftime("%H.%M")}, duration {reservation.duration} h, {reservation.resource}')


def confirmation_statuses(reservations: list[Reservation]) -> None:
    """
    Print confirmation statuses

    Parameters:
     reservations (list): Reservations
    """
    for reservation in reservations[1:]:
        name : str = reservation.name
        confirmed : bool = reservation.is_confirmed()

        print(f'{name} → {"Confirmed" if confirmed else "NOT Confirmed"}')

def confirmation_summary(reservations: list[Reservation]) -> None:
    """
    Print confirmation summary

    Parameters:
     reservations (list): Reservations
    """
    confirmed : int = len([x for x in reservations[1:] if x.is_confirmed()])
    print(f'- Confirmed reservations: {confirmed} pcs\n- Not confirmed reservations: {len(reservations) - confirmed} pcs')

def total_revenue(reservations: list[Reservation]) -> None:
    """
    Print total revenue

    Parameters:
     reservations (list): Reservations
    """
    revenue : float = sum(x.total_price() for x in reservations[1:] if x.is_confirmed())
    print(f'Total revenue from confirmed reservations: {revenue:.2f} €'.replace('.', ','))

def main():
    """
    Prints reservation information according to requirements
    Reservation-specific printing is done in functions
    """
    reservations = fetch_reservations("reservations.txt")
    print("1) Confirmed Reservations")
    confirmed_reservations(reservations)
    print("2) Long Reservations (≥ 3 h)")
    long_reservations(reservations)
    print("3) Reservation Confirmation Status")
    confirmation_statuses(reservations)
    print("4) Confirmation Summary")
    confirmation_summary(reservations)
    print("5) Total Revenue from Confirmed Reservations")
    total_revenue(reservations)

if __name__ == "__main__":
    main()

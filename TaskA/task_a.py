# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by Sara Grankvist according to given task

"""
Program that reads reservation details from a file
and prints them to the console:

Reservation number: 123
Booker: Anna Virtanen
Date: 31.10.2025
Start time: 10.00
Number of hours: 2
Hourly price: 19,95 €
Total price: 39,90 €
Paid: Yes
Location: Meeting Room A
Phone: 0401234567
Email: anna.virtanen@example.com
"""

from datetime import datetime

def main():
    # Define the file name directly in the code
    reservations = "reservations.txt"

    # Open the file and read its contents
    with open(reservations, "r", encoding="utf-8") as f:
        reservation = f.read().strip()

    # Split the reservation string into a list
    reservation = reservation.split('|')

    # Start adding list contents into variables for formatting
    reservation_number = int(reservation[0])
    booker = reservation[1] # Already a string so no need for type conversion
    
    # Convert the date and time to Finnish format:
    booking_date = datetime.strptime(reservation[2], "%Y-%m-%d").date()
    booking_date_fin = booking_date.strftime("%d.%m.%Y")
    booking_time = datetime.strptime(reservation[3], "%H:%M").time()
    booking_time_fin = booking_time.strftime("%H.%M")
    hours = int(reservation[4])
    hour_price = float(reservation[5])

    # Calcutale the total price
    total_price = hours * hour_price
    
    # Format prices into string with 2 decimals and comma as decimal separator:
    hour_price_str = f"{hour_price:.2f}".replace('.', ',')
    total_price_str = f"{total_price:.2f}".replace('.', ',')
    
    paid = bool(reservation[6])
    resource = reservation[7]
    phone_number = reservation[8]
    email_address = reservation[9]


    # Print reservation details to console
    print("Reservation number: " + str(reservation_number))
    print("Booker: " + booker)
    print("Date: " + booking_date_fin)
    print("Start time: " + booking_time_fin)
    print("Number of hours: " + str(hours))
    print("Hourly price: " + hour_price_str + " €")
    print("Total price: " + total_price_str + " €")
    print(f"Paid: {'Yes' if paid else 'No'}")
    print("Location: " + resource)
    print("Phone: " + phone_number)
    print("Email: " + email_address) 

if __name__ == "__main__":
    main()
import datetime
import random
from faker import Faker
import mysql.connector

fake = Faker()
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sree@mysql#",
    database="cab"
)
cursor = connection.cursor()

used_emails = set()
# # Generate data for Locations table (Primary Key)
for location_id in range(1, 101):  # At least 100 locations
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    address = fake.address()
    insert_query = f"INSERT INTO Locations (location_id, latitude, longitude, address) VALUES ({location_id}, {latitude}, {longitude}, '{address}')"
    cursor.execute(insert_query)
    connection.commit()

# Generate data for Riders table (Primary Key)
for rider_id in range(1, 1001):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = None
    while email is None or email in used_emails:
        email = fake.email()
    used_emails.add(email)
    phone_number = "9" + str(fake.random_int(min=100000000, max=999999999))
    dob = fake.date_of_birth()
    dl_expiry = fake.future_date(end_date="+5y")
    insurance_expiry = fake.future_date(end_date="+3y")
    insert_query = f"INSERT INTO Riders (rider_id, first_name, last_name, email, phone_number, date_of_birth, dl_expiry_date, insurance_expiry_date) VALUES ({rider_id}, '{first_name}', '{last_name}', '{email}', '{phone_number}', '{dob}', '{dl_expiry}', '{insurance_expiry}')"
    cursor.execute(insert_query)
    connection.commit()

#Generate data for Drivers table (Primary Key)
for driver_id in range(1, 101):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = None
    while email is None or email in used_emails:
        email = fake.email()
    used_emails.add(email)
    phone_number = "9" + str(fake.random_int(min=100000000, max=999999999))
    dob = fake.date_of_birth()

    # Generate more future dates and fewer past dates for dl_expiry and insurance_expiry
    today = datetime.date.today()
    dl_expiry = fake.date_between_dates(date_start=today + datetime.timedelta(days=1),
                                        date_end=today + datetime.timedelta(days=365 * 5))
    insurance_expiry = fake.date_between_dates(date_start=today + datetime.timedelta(days=1),
                                               date_end=today + datetime.timedelta(days=365 * 3))

    insert_query = f"INSERT INTO Drivers (driver_id, first_name, last_name, email, phone_number, date_of_birth, dl_expiry_date, insurance_expiry_date) VALUES ({driver_id}, '{first_name}', '{last_name}', '{email}', '{phone_number}', '{dob}', '{dl_expiry}', '{insurance_expiry}')"

    # Execute and commit the query
    cursor.execute(insert_query)
    connection.commit()

for driver_id in range(101, 151):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = None
    while email is None or email in used_emails:
        email = fake.email()
    used_emails.add(email)
    phone_number = "9" + str(fake.random_int(min=100000000, max=999999999))
    dob = fake.date_of_birth()

    # Generate past dates for dl_expiry and insurance_expiry
    today = datetime.date.today()
    dl_expiry = fake.date_between_dates(date_start=today - datetime.timedelta(days=365 * 10),
                                        date_end=today - datetime.timedelta(days=1))
    insurance_expiry = fake.date_between_dates(date_start=today - datetime.timedelta(days=365 * 5),
                                               date_end=today - datetime.timedelta(days=1))

    insert_query = f"INSERT INTO Drivers (driver_id, first_name, last_name, email, phone_number, date_of_birth, dl_expiry_date, insurance_expiry_date) VALUES ({driver_id}, '{first_name}', '{last_name}', '{email}', '{phone_number}', '{dob}', '{dl_expiry}', '{insurance_expiry}')"

    # Execute and commit the query
    cursor.execute(insert_query)
    connection.commit()




# Generate data for Vehicles table (Primary Key)
vehicle_companies = [
    "Toyota", "Ford", "Honda", "Chevrolet", "BMW", "Mercedes-Benz",
    "Audi", "Nissan", "Volkswagen", "Tesla", "Hyundai", "Volvo",
    "Mazda", "Kia", "Subaru", "Lexus", "Porsche", "Jeep", "Ferrari", "Jaguar"
]

vehicle_models = {
    "Toyota": ["Camry", "Corolla", "Rav4", "Highlander", "Prius"],
    "Ford": ["Mustang", "F-150", "Focus", "Escape", "Explorer"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Fit"],
    "Chevrolet": ["Cruze", "Malibu", "Equinox", "Silverado", "Traverse"],
    "BMW": ["X3", "X5", "3 Series", "5 Series", "7 Series"],
    "Mercedes-Benz": ["C-Class", "E-Class", "S-Class", "GLC", "GLE"],
    "Audi": ["A3", "A4", "Q5", "Q7", "TT"],
    "Nissan": ["Altima", "Maxima", "Rogue", "Murano", "Pathfinder"],
    "Volkswagen": ["Jetta", "Passat", "Golf", "Tiguan", "Atlas"],
    "Tesla": ["Model S", "Model 3", "Model X", "Model Y"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe", "Kona"],
    "Volvo": ["S60", "S90", "XC40", "XC60", "XC90"],
    "Mazda": ["Mazda3", "Mazda6", "CX-5", "CX-9"],
    "Kia": ["Forte", "Optima", "Sportage", "Sorento", "Telluride"],
    "Subaru": ["Impreza", "Legacy", "Outback", "Forester", "Ascent"],
    "Lexus": ["ES", "RX", "NX", "LS", "GX"],
    "Porsche": ["911", "Cayenne", "Panamera", "Macan"],
    "Jeep": ["Wrangler", "Grand Cherokee", "Cherokee", "Compass", "Renegade"],
    "Ferrari": ["488 GTB", "812 Superfast", "F8 Tributo", "SF90 Stradale"],
    "Jaguar": ["XE", "XF", "F-PACE", "E-PACE", "I-PACE"]
}



vehicle_types = ["Sedan", "SUV", "Van", "Coupe", "Convertible", "Electric"]

# Generate data for Vehicles table
for vehicle_id in range(1, 501):
    driver_id = random.randint(1, 150)  # Assuming 150 drivers
    vehicle_company = random.choice(vehicle_companies)
    vehicle_type = random.choice(vehicle_types)
    license_plate = fake.random_int(min=1000, max=9999)
    make = vehicle_company
    model = random.choice(vehicle_models[vehicle_company])
    insert_query = f"INSERT INTO Vehicles (vehicle_id, driver_id, vehicle_type, license_plate, make, model) VALUES ({vehicle_id}, {driver_id}, '{vehicle_type}', '{license_plate}', '{make}', '{model}')"
    cursor.execute(insert_query)
    connection.commit()

# Generate data for Trips table (Primary Key)
for trip_id in range(1, 2001):
    driver_id = random.randint(1, 150)  # Assuming 150 drivers
    rider_id = random.randint(1, 1000)  # Assuming 1000 riders
    vehicle_id = random.randint(1, 500)  # Assuming 500 vehicles
    start_location_id = random.randint(1, 100)  # Assuming 100 locations
    end_location_id = random.randint(1, 100)  # Assuming 100 locations
    start_time = fake.date_time_this_year()
    end_time = fake.date_time_this_year()
    fare_amount = round(random.uniform(5, 50), 2)
    insert_query = f"INSERT INTO Trips (trip_id, driver_id, rider_id, vehicle_id, start_location_id, end_location_id, start_time, end_time, fare_amount) VALUES ({trip_id}, {driver_id}, {rider_id}, {vehicle_id}, {start_location_id}, {end_location_id}, '{start_time}', '{end_time}', {fare_amount})"
    cursor.execute(insert_query)
    connection.commit()

# Generate data for PaymentInformation table (Primary Key)
for rider_id in range(1, 1001):
    card_number = fake.credit_card_number(card_type="mastercard")
    expiration_date = fake.credit_card_expire()
    cvv = fake.credit_card_security_code(card_type="mastercard")
    insert_query = f"INSERT INTO PaymentInformation (payment_id, user_id, card_number, expiration_date, cvv) VALUES ({rider_id}, {rider_id}, '{card_number}', '{expiration_date}', '{cvv}')"
    cursor.execute(insert_query)
    connection.commit()
ride_comments = [
    "Smooth ride, great driver!",
    "Excellent service, arrived on time.",
    "Clean car and comfortable ride.",
    "Driver was professional and courteous.",
    "Fast and efficient ride.",
    "Highly recommended!",
    "Ride was pleasant and safe.",
    "Great experience overall.",
    "Impressed with the service.",
    "Enjoyed the journey.",
    "Service exceeded my expectations.",
    "Car was in excellent condition.",
    "Driver helped with luggage.",
    "Driver was knowledgeable about the area.",
    "Arrived at my destination on time.",
    "Driver was attentive and focused."
    "Average ride, nothing remarkable.",
    "Service was okay, nothing special.",
    "Ride was decent, not great.",
    "Driver was alright, nothing outstanding.",
    "Average experience overall.",
    "Car was fine, ride was average.",
    "Neutral feelings about the ride.",
    "Service met my basic expectations.",
    "Neither good nor bad.",
    "It was a standard ride.",
    "Middle-of-the-road service."
]
# Generate data for Ratings table (Primary Key)
for rating_id in range(1, 3001):
    trip_id = random.randint(1, 2000)  # Assuming 2000 trips
    rider_id = random.randint(1, 1000)  # Assuming 1000 riders
    driver_id = random.randint(1, 150)  # Assuming 150 drivers
    rating = round(random.uniform(3, 5), 1)
    comment = random.choice(ride_comments)
    insert_query = f"INSERT INTO Ratings (rating_id, trip_id, rider_id, driver_id, rating, comment) VALUES ({rating_id}, {trip_id}, {rider_id}, {driver_id}, {rating}, '{comment}')"
    cursor.execute(insert_query)
    connection.commit()

cursor.close()
connection.close()

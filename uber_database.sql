CREATE DATABASE cab;
USE cab;

-- Create Riders table
CREATE TABLE Riders (
    rider_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(15),
    date_of_birth DATE,
    dl_expiry_date DATE,
    insurance_expiry_date DATE
);

-- Create Drivers table
CREATE TABLE Drivers (
    driver_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(15),
    date_of_birth DATE,
    dl_expiry_date DATE,
    insurance_expiry_date DATE
);

-- Create Vehicles table
CREATE TABLE Vehicles (
    vehicle_id INT PRIMARY KEY,
    driver_id INT,
    vehicle_type VARCHAR(50),
    license_plate VARCHAR(20),
    make VARCHAR(50),
    model VARCHAR(50),
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id)
);

-- Create Trips table
CREATE TABLE Trips (
    trip_id INT PRIMARY KEY,
    driver_id INT,
    rider_id INT,
    vehicle_id INT,
    start_location_id INT,
    end_location_id INT,
    start_time DATETIME,
    end_time DATETIME,
    fare_amount DECIMAL(10, 2),
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id),
    FOREIGN KEY (rider_id) REFERENCES Riders(rider_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id),
    FOREIGN KEY (start_location_id) REFERENCES Locations(location_id),
    FOREIGN KEY (end_location_id) REFERENCES Locations(location_id)
);

-- Create Payment Information table
CREATE TABLE PaymentInformation (
    payment_id INT PRIMARY KEY,
    user_id INT,
    card_number VARCHAR(16),
    expiration_date VARCHAR(7),
    cvv VARCHAR(4),
    FOREIGN KEY (user_id) REFERENCES Riders(rider_id)
);

-- Create Locations table
CREATE TABLE Locations (
    location_id INT PRIMARY KEY,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    address VARCHAR(255)
);

-- Create Ratings table
CREATE TABLE Ratings (
    rating_id INT PRIMARY KEY,
    trip_id INT,
    rider_id INT,
    driver_id INT,
    rating DECIMAL(2, 1),
    comment TEXT,
    FOREIGN KEY (trip_id) REFERENCES Trips(trip_id),
    FOREIGN KEY (rider_id) REFERENCES Riders(rider_id),
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id)
);



DELIMITER //

CREATE PROCEDURE CalculateAverageDriverRating(IN driverId INT, OUT averageRating DECIMAL(3, 2))
BEGIN
    SELECT AVG(rating)
    INTO averageRating
    FROM Ratings
    WHERE driver_id = driverId;
END //

DELIMITER ;


-- Create the DL_Expiry_Log table to store the log information
CREATE TABLE DL_Expiry_Log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id INT,
    expiry_date DATE,
    log_timestamp DATETIME
);

-- Create the CheckDLExpiry trigger
DELIMITER //
CREATE TRIGGER CheckDLExpiry
BEFORE INSERT ON Drivers
FOR EACH ROW
BEGIN
    IF NEW.dl_expiry_date <= CURDATE() THEN
        -- Insert a record into the DL_Expiry_Log table
        INSERT INTO DL_Expiry_Log (driver_id, expiry_date, log_timestamp)
        VALUES (NEW.driver_id, NEW.dl_expiry_date, NOW());
    END IF;
END //
DELIMITER ;


-- Create the Insurance_Expiry_Log table to store the log information
CREATE TABLE Insurance_Expiry_Log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id INT,
    expiry_date DATE,
    log_timestamp DATETIME
);

-- Create the CheckInsuranceExpiry trigger
DELIMITER //
CREATE TRIGGER CheckInsuranceExpiry
BEFORE INSERT ON Drivers
FOR EACH ROW
BEGIN
    IF NEW.insurance_expiry_date <= CURDATE() THEN
        -- Insert a record into the Insurance_Expiry_Log table
        INSERT INTO Insurance_Expiry_Log (driver_id, expiry_date, log_timestamp)
        VALUES (NEW.driver_id, NEW.insurance_expiry_date, NOW());
    END IF;
END //
DELIMITER ;





-- Create a new table by joining all relevant information
CREATE TABLE AllData AS
SELECT
    T.trip_id,
    R.rider_id,
    R.first_name AS rider_first_name,
    R.last_name AS rider_last_name,
    R.email AS rider_email,
    R.phone_number AS rider_phone_number,
    R.date_of_birth AS rider_date_of_birth,
    D.driver_id,
    D.first_name AS driver_first_name,
    D.last_name AS driver_last_name,
    D.email AS driver_email,
    D.phone_number AS driver_phone_number,
    D.date_of_birth AS driver_date_of_birth,
    V.vehicle_id,
    V.vehicle_type,
    V.license_plate,
    V.make AS vehicle_make,
    V.model AS vehicle_model,
    SL.location_id AS start_location_id,
    SL.latitude AS start_latitude,
    SL.longitude AS start_longitude,
    SL.address AS start_address,
    EL.location_id AS end_location_id,
    EL.latitude AS end_latitude,
    EL.longitude AS end_longitude,
    EL.address AS end_address,
    T.start_time,
    T.end_time,
    T.fare_amount,
    Ra.rating,
    Ra.comment,
    Dl.expiry_date AS dl_expiry,
    Ins.expiry_date AS insurance_expiry
FROM Trips AS T
JOIN Riders AS R ON T.rider_id = R.rider_id
JOIN Drivers AS D ON T.driver_id = D.driver_id
LEFT JOIN Ratings AS Ra ON T.trip_id = Ra.trip_id
LEFT JOIN dl_expiry_log AS Dl ON D.driver_id = Dl.driver_id
LEFT JOIN insurance_expiry_log AS Ins ON D.driver_id = Ins.driver_id
JOIN Vehicles AS V ON T.vehicle_id = V.vehicle_id
JOIN Locations AS SL ON T.start_location_id = SL.location_id
JOIN Locations AS EL ON T.end_location_id = EL.location_id;



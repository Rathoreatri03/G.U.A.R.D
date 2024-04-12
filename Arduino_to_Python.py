import serial
import time
import numpy as np

# Establish serial connection with Arduino Uno
ser = serial.Serial('COM11', 9600)  # Adjust the COM port as necessary

# Wait for the Arduino to initialize
time.sleep(2)

# Variables for storing calibrated reference values
avg_accel_x = 0
avg_accel_y = 0
avg_accel_z = 0
avg_gyro_x = 0
avg_gyro_y = 0
avg_gyro_z = 0

# Thresholds for detecting movement and accidents
orientation_threshold = 10  # Adjust as needed based on calibration

# Function to calculate dynamic threshold for movement detection
def calculate_threshold(accel_values):
    # Calculate standard deviation of accelerometer readings
    std_dev = np.std(accel_values)
    # Use a multiple of standard deviation as the threshold
    threshold = 2 * std_dev  # Adjust multiplier as needed
    return threshold

# Function to check for vehicle movement
def check_movement(current_accel_x, current_accel_y, current_accel_z):
    global avg_accel_x, avg_accel_y, avg_accel_z
    # Calculate current acceleration magnitude
    current_accel_mag = (current_accel_x**2 + current_accel_y**2 + current_accel_z**2)**0.5
    # Calculate difference between current and average accelerations
    accel_diff = abs(current_accel_mag - (avg_accel_x**2 + avg_accel_y**2 + avg_accel_z**2)**0.5)
    # Check if the difference exceeds the dynamic threshold
    threshold = calculate_threshold([current_accel_x, current_accel_y, current_accel_z])
    if accel_diff > threshold:
        print("Vehicle is moving!")

# Function to check for accidents (flips)
def check_accident(current_gyro_x, current_gyro_y, current_gyro_z):
    global avg_gyro_x, avg_gyro_y, avg_gyro_z
    # Calculate difference between current and average gyroscope values
    gyro_diff_x = abs(current_gyro_x - avg_gyro_x)
    gyro_diff_y = abs(current_gyro_y - avg_gyro_y)
    gyro_diff_z = abs(current_gyro_z - avg_gyro_z)
    # Check if any orientation change exceeds the threshold
    if gyro_diff_x > orientation_threshold or gyro_diff_y > orientation_threshold or gyro_diff_z > orientation_threshold:
        print("Vehicle is flipped! Accident occurred.")

# Main loop for processing data after calibration
print("Starting main loop...")
while True:
    # Read data from serial port
    data = ser.readline().decode().strip()

    # Split the data into individual values
    values = data.split(",")

    # Extract accelerometer and gyroscope values
    current_accel_x = float(values[0].split(":")[1])
    current_accel_y = float(values[1].split(":")[1])
    current_accel_z = float(values[2].split(":")[1])
    current_gyro_x = float(values[3].split(":")[1])
    current_gyro_y = float(values[4].split(":")[1])
    current_gyro_z = float(values[5].split(":")[1])

    # Check for vehicle movement
    check_movement(current_accel_x, current_accel_y, current_accel_z)

    # Check for accidents (flips)
    check_accident(current_gyro_x, current_gyro_y, current_gyro_z)

    # Print the received data for verification
    print("Acceleration - X:", current_accel_x, " Y:", current_accel_y, " Z:", current_accel_z)
    print("Gyroscope - X:", current_gyro_x, " Y:", current_gyro_y, " Z:", current_gyro_z)
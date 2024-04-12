void setup() {
  // Start serial communication
  Serial.begin(9600);
  // Seed random number generator
  randomSeed(analogRead(0));
}

void loop() {
  // Simulate accelerometer and gyroscope readings
  float accel_x = random(-100, 100) / 100.0; // Range: -1.00 to 1.00
  float accel_y = random(-100, 100) / 100.0; // Range: -1.00 to 1.00
  float accel_z = random(-100, 100) / 100.0; // Range: -1.00 to 1.00
  float gyro_x = random(-100, 100) / 100.0;  // Range: -1.00 to 1.00
  float gyro_y = random(-100, 100) / 100.0;  // Range: -1.00 to 1.00
  float gyro_z = random(-100, 100) / 100.0;  // Range: -1.00 to 1.00

  // Send sensor readings over serial
  Serial.print("AccelX:");
  Serial.print(accel_x);
  Serial.print(",AccelY:");
  Serial.print(accel_y);
  Serial.print(",AccelZ:");
  Serial.print(accel_z);
  Serial.print(",GyroX:");
  Serial.print(gyro_x);
  Serial.print(",GyroY:");
  Serial.print(gyro_y);
  Serial.print(",GyroZ:");
  Serial.println(gyro_z);

  // Delay for stability (adjust as needed)
  delay(1000);
}

// Ultrasonic Sensor Test Code (HC-SR04)
// Author: Caio + Copilot
// Purpose: Verify sensor readings and serial output

const int trigPin = 12;
const int echoPin = 13;

long duration;
int distance;

void setup() {
  Serial.begin(19200);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Clear the trigger
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  delayMicroseconds(2);

  // Send a 10 µs pulse to trigger
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read echo pulse duration
  duration = pulseIn(echoPin, HIGH);

  // Convert to distance (cm)
  distance = duration * 0.034 / 2;

  // Print results
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(50);
}

#include "mp6550_driver.hpp"

// RC receiver channel pins
// CHANGE THESE to match actual wiring i think they right tho
const int ch1Pin = 7;
const int ch2Pin = 3;
const int ch3Pin = 6;
const int ch4Pin = 8;

// RC pulse values, sqaure in deadzone
unsigned long ch1Value = 1500;
unsigned long ch2Value = 1500;
unsigned long ch3Value = 1500;
unsigned long ch4Value = 1500;

// da Motor driver pins
// format: motor(IN1, IN2, SLP)
// change to match actual wiring, dont touch it!!!!
motor motor1(10, 11, 4);
motor motor2(5, 9, 2);
float speedmod = 0.6;

void setup() {
  pinMode(ch1Pin, INPUT);
  pinMode(ch2Pin, INPUT);
  pinMode(ch3Pin, INPUT);
  pinMode(ch4Pin, INPUT);
  Serial.begin(19200);
}

void loop() {
  ch1Value = pulseIn(ch1Pin, HIGH, 25000);
  ch4Value = pulseIn(ch4Pin, HIGH, 25000);
  ch3Value = pulseIn(ch3Pin, HIGH, 25000);
  ch2Value = pulseIn(ch2Pin, HIGH, 25000);

  delay(100);

  // Stop motors if CH1 or CH3 signal is lost
  if (ch1Value == 0 || ch3Value == 0) {
    motor1.brake();
    motor2.brake();
    return;
  }
  // 1. FORWARD
  else if (ch3Value > 1550) {
    float percent_pulled = (ch3Value - 1550.0) / (2000.0 - 1550.0);
    float motorSpeed = percent_pulled * 255 * speedmod;  
    
    Serial.print("FORWARD MOVING AT: "); Serial.println(motorSpeed);  
    motor1.forwards(motorSpeed);
    motor2.forwards(motorSpeed);
  }
  // 2. BACKWARD
  else if (ch3Value < 1450) {
    float percent_pulled = (1450.0 - ch3Value) / (1450.0 - 1000.0);
    float motorSpeed = percent_pulled * 255 * speedmod;
    
    Serial.print("BACK MOVING AT: "); Serial.println(motorSpeed);  
    motor1.backwards(motorSpeed);
    motor2.backwards(motorSpeed);
  }
  // 3. RIGHT TURN
  else if (ch1Value > 1550) {
    float percent_pulled = (ch1Value - 1550.0) / (2000.0 - 1550.0);
    float motorSpeed = percent_pulled * 255 * speedmod;
    
    Serial.print("RIGHT MOVING AT: "); Serial.println(motorSpeed);  
    motor1.forwards(motorSpeed);
    motor2.backwards(motorSpeed);
  }
  // 4. LEFT TURN
  else if (ch1Value < 1450) {
    float percent_pulled = (1450.0 - ch1Value) / (1450.0 - 1000.0);
    float motorSpeed = percent_pulled * 255 * speedmod;
    
    Serial.print("LEFT MOVING AT: "); Serial.println(motorSpeed);
    motor1.backwards(motorSpeed);
    motor2.forwards(motorSpeed);
  }
  // 5. STOP (Both controls centered)
  else {
    motor1.brake();
    motor2.brake();
  }
}

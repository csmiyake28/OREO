#include "mp6550_driver.hpp"

const int pwm1 = 1;
const int dir1 = 2;

const int pwm2 = 3;
const int dir2 = 4;

// hello

//TEST TEST CAIO pUSH!

//hi ty alive! or tylenol

// woahhh This is CAIO testing

const int ch1Pin = 5;  // Signal wire connected to Digital Pin 2
const int ch2Pin = 6;  // Signal wire connected to Digital Pin 3
const int ch3Pin = 7;
const int ch4Pin = 8;



void setup() {
  // put your setup code here, to run once:
  pinMode(ch1Pin, INPUT);
  pinMode(ch2Pin, INPUT);
  pinMode(ch3Pin, INPUT);
  pinMode(ch4Pin, INPUT);

  pinMode(pwm1, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(pwm2, OUTPUT);
  pinMode(dir2, OUTPUT);



  //TESTING PULL
}

void loop() {
  // put your main code here, to run repeatedly:

  ch1Value = pulseIn(ch1Pin, HIGH, 25000);
  ch4Value = pulseIn(ch4Pin, HIGH, 25000);
  ch3Value = pulseIn(ch3Pin, HIGH, 25000);
  ch2Value = pulseIn(ch2Pin, HIGH, 25000);


  //Debugging seeing the rawCH1 & rawCh3

  delay(67);

  //testing testing!
}

/*
		Library for MP6550 DC-Motordriver
*/

#include "mp6550_driver.hpp"
#include <Arduino.h>

motor::motor(int IN1pin, int IN2pin, int SLPpin){

 	IN1 = IN1pin;
	IN2 = IN2pin;
	SLP = SLPpin;

	pinMode(IN1, OUTPUT);
	pinMode(IN2, OUTPUT);
	pinMode(SLP, OUTPUT);

	digitalWrite(IN1, LOW);
	digitalWrite(IN2, LOW);
	digitalWrite(SLP, HIGH);
	speed_ = 0;
	dir_ = 0;
	br_speed_ = 255;
	sleep_ = 0;
}

void motor::forwards(){
	digitalWrite(IN1, HIGH);
	analogWrite(IN2, speed_);
	dir_	=  1;
}

void motor::forwards(int speed){
	setSpeed(speed);
	forwards();
}

void motor::backwards(){
	digitalWrite(IN2, HIGH);
	analogWrite(IN1, speed_);
	dir_ = -1;
}

void motor::backwards(int speed){
	setSpeed(speed);
	backwards();
}

void motor::brake(){
	if(dir_ == 1){
		digitalWrite(IN1, HIGH);
		analogWrite(IN2, br_speed_);
	}
	else if(dir_ == -1){
		digitalWrite(IN2, HIGH);
		analogWrite(IN2, br_speed_);
  }
	else{
		digitalWrite(IN1, HIGH);
		digitalWrite(IN2, HIGH);
	}
	delay(100);
	digitalWrite(IN1, LOW);
	digitalWrite(IN2, LOW);
	dir_ = 0;
}

void motor::brake(int br_speed){
	setBrakeSpeed(br_speed);
	brake();
}

void motor::setBrakeSpeed(int br_speed){
	if(br_speed>255)br_speed = 255;
	else if(br_speed<0)br_speed = 0;

	br_speed_ = br_speed;
}

void motor::toggleDir(){
	if(sleep_ == 0){
		if(dir_ == 1) backwards();
		else if(dir_ == -1) forwards();
		else brake();
 }
	else dir_ =	-dir_;
}

void motor::setSpeed(int speed){
	if(speed>255)speed =	255;
	else if(speed<0)speed = 0;
	speed_ =	255- speed;	//One Pin High and One Pin Low is highest speed - thus 255 - speed -> speed input = 255 -> speed_ = 0 -> max speed
}

int motor::getSpeed(){
	return 255-speed_;
}

int motor::getBrakeSpeed(){
	return br_speed_;
}

int motor::getStbyStat(){
	return sleep_;
}

void motor::sleep(){
	brake();
	digitalWrite(SLP,LOW);
	sleep_ = 1;
}

void motor::sleep(int secs){
	sleep();
	delay(secs*1000);
	wakeUp();
}

void motor::wakeUp(){
	digitalWrite(SLP, HIGH);
	sleep_ = 0;
}

motor::~motor(){
	brake();
	delay(500);
	digitalWrite(SLP, LOW);
}

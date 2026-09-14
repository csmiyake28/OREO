#ifndef MP6550_driver_hpp
#define MP6550_driver_hpp

class motor{
	private:
		int speed_;		  //Integer for pwm-speed (255 = 0 speed | 0 = max Speed)
		int br_speed_;	//Integer for Brake_speed (255 = max Brake | 0 = No Break)
		int dir_;				//Integer for Direction (-1 = backwards | 0 = idle | 1 = forwards)
		int sleep_;
		int IN1;				//Pin connected to IN1
		int IN2;				//Pin connected to IN2
		int SLP;			   //Pin connected to SLP

	public:
		motor(int IN1pin, int IN2pin, int SLPpin);	//Constructor with default: Sleep, In1,In2=0, speed = 0, br_speed = 0; standby = 1; dir_ = 0
		void forwards();	//Motor moves forwards with already set speed_
		void forwards(int speed);	//Motor moves forwards with given speed
		void backwards();	//Motor moves backwards with already set speed_
		void backwards(int speed);	//Motor moves backwards with given speed
		void brake();			//Motor brakes with already set br_speed_
		void brake(int br_speed);	//Motor brakes with given speed br_speed
		void setBrakeSpeed(int br_speed);	//Sets Brake speed of Motor ( 0 = no brake | 255 = max brake)
		void toggleDir();	//Toggle direction of Motor
		void setSpeed(int speed);	//Sets speed for Motor (255 = Max Speed | 0 = no Speed)
		int getSpeed();						//Gets speed of Motor (same as line above)
		int getBrakeSpeed();	//Gets brake speed of Motor
		int getStbyStat();					//Gets Sleep State of Motor (Status mentioned standby_)
		void sleep();							//Puts Driver to Sleep
		void sleep(int secs);			//Puts Driver to Sleep for int secs (seconds)
		void wakeUp();					//Wakes Driver up
		~motor();							//Destructor -> Brakes first then enables SLP
};

#endif

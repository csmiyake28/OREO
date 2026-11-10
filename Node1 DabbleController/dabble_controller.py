# ************************************************************
# File name: dabble_controller.py
# Purpose: Digital Dabble Gamepad Controller
# Future integration: Orange Pi + ROS 2
# ************************************************************

# Convert controller inputs into robot commands
def process_command(command):

    if command == "UP":
        print("Robot moving FORWARD")

    elif command == "DOWN":
        print("Robot moving BACKWARD")

    elif command == "LEFT":
        print("Robot turning LEFT")

    elif command == "RIGHT":
        print("Robot turning RIGHT")

    elif command == "STOP":
        print("Robot STOPPED")

    else:
        print("Invalid command")


# Simulate Dabble Gamepad using keyboard
def keyboard_controller():

    print("Dabble Digital Controller")
    print("-------------------------")
    print("W = Forward")
    print("S = Backward")
    print("A = Left")
    print("D = Right")
    print("X = Stop")
    print("Q = Quit")
    print("-------------------------")

    while True:

        key = input("Enter command: ").lower()

        if key == "w":
            process_command("UP")

        elif key == "s":
            process_command("DOWN")

        elif key == "a":
            process_command("LEFT")

        elif key == "d":
            process_command("RIGHT")

        elif key == "x":
            process_command("STOP")

        elif key == "q":
            process_command("STOP")
            print("Controller disconnected")
            break

        else:
            print("Unknown input")


# Main program
if __name__ == "__main__":
    keyboard_controller()
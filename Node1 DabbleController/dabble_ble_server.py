# ************************************************************
# File name: dabble_ble_server.py
# Purpose: BLE server for Dabble digital Gamepad
# Hardware: Orange Pi Zero 3W
# Operating System: Linux
# Future integration: ROS 2
# ************************************************************

import sys

from dabble_bluetooth import DabbleReceiver


# Bluetooth configuration
DEVICE_NAME = "OrangePi_Dabble"

SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"

RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

TX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


# Create the Dabble receiver
receiver = DabbleReceiver()


# Handle data received from the Bluetooth characteristic
def on_ble_data(data):

    print("BLE data received:", data.hex(" ").upper())

    receiver.receive_data(data)


# Check operating system
def check_platform():

    if sys.platform != "linux":

        print("This BLE server requires Linux.")
        print("Current platform:", sys.platform)
        print("Simulation mode is available on Windows.")

        return False

    print("Linux detected.")
    print("Preparing BlueZ Bluetooth server...")

    return True


# Test the BLE data callback
def test_ble_callback():

    print("\nTesting BLE callback")

    test_packet = bytes.fromhex(
        "FF 01 01 01 02 00 01 00"
    )

    on_ble_data(test_packet)

    receiver.disconnect()


# Main program
if __name__ == "__main__":

    print("Dabble BLE Server")
    print("-------------------------")

    print("Device name:", DEVICE_NAME)
    print("Service UUID:", SERVICE_UUID)

    if check_platform():
        print("Linux BLE GATT server not implemented yet.")

    else:
        test_ble_callback()
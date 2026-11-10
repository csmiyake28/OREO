# ************************************************************
# File name: dabble_bluetooth.py
# Purpose: Receive and process Dabble Bluetooth data
# Hardware: Orange Pi Zero 3W
# Future integration: ROS 2
# ************************************************************

import time

from dabble_decoder import decode_packet
from dabble_controller import process_command


# Configuration
PACKET_LENGTH = 8
START_FRAME = 0xFF
COMMAND_TIMEOUT = 0.5  # Seconds


class DabbleReceiver:

    def __init__(self):

        self.buffer = bytearray()
        self.last_packet_time = None
        self.current_command = "STOP"

    # Process a decoded command
    def update_command(self, command):

        if command != self.current_command:

            self.current_command = command
            process_command(command)

    # Receive incoming Bluetooth bytes
    def receive_data(self, data):

        self.buffer.extend(data)

        # Search for complete packets
        while len(self.buffer) >= PACKET_LENGTH:

            # Find the beginning of a packet
            if self.buffer[0] != START_FRAME:
                self.buffer.pop(0)
                continue

            # Extract possible packet
            packet = bytes(self.buffer[:PACKET_LENGTH])

            # Decode packet
            command = decode_packet(packet)

            if command is not None:

                print("Received:", packet.hex(" ").upper())
                print("Command:", command)

                self.last_packet_time = time.monotonic()

                self.update_command(command)

                # Remove processed packet
                del self.buffer[:PACKET_LENGTH]

            else:

                # Invalid packet: search for next start
                self.buffer.pop(0)

    # Stop robot if communication is lost
    def check_timeout(self):

        if self.last_packet_time is None:
            return

        elapsed = time.monotonic() - self.last_packet_time

        if elapsed > COMMAND_TIMEOUT:

            if self.current_command != "STOP":

                print("Communication timeout!")
                self.update_command("STOP")

            self.last_packet_time = None

    # Handle Bluetooth disconnection
    def disconnect(self):

        print("Bluetooth disconnected")

        self.buffer.clear()
        self.last_packet_time = None

        self.update_command("STOP")


# Simulate receiving Bluetooth data
def test_bluetooth():

    receiver = DabbleReceiver()

    print("Dabble Bluetooth Receiver")
    print("-------------------------")

    # Simulate UP packet arriving in three chunks
    print("\nTesting fragmented packet:")

    receiver.receive_data(bytes.fromhex("FF 01 01"))

    receiver.receive_data(bytes.fromhex("01 02 00"))

    receiver.receive_data(bytes.fromhex("01 00"))

    # Simulate RIGHT command
    print("\nTesting RIGHT:")

    receiver.receive_data(
        bytes.fromhex("FF 01 01 01 02 00 08 00")
    )

    # Simulate STOP command
    print("\nTesting STOP:")

    receiver.receive_data(
        bytes.fromhex("FF 01 01 01 02 00 00 00")
    )

    # Simulate lost connection while moving
    print("\nTesting communication timeout:")

    receiver.receive_data(
        bytes.fromhex("FF 01 01 01 02 00 01 00")
    )

    # No new packets arrive
    time.sleep(0.6)

    receiver.check_timeout()

    print("\nTest completed!")


# Main program
if __name__ == "__main__":
    test_bluetooth()
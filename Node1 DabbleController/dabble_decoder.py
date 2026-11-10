# ************************************************************
# File name: dabble_decoder.py
# Purpose: Decode digital Dabble Gamepad Bluetooth packets
# Future integration: Orange Pi + ROS 2
# ************************************************************

from dabble_controller import process_command


# Dabble protocol constants
START_FRAME = 0xFF
END_FRAME = 0x00
GAMEPAD_ID = 0x01
DIGITAL_MODE = 0x01


# Decode directional button bits
def decode_buttons(up, down, left, right):

    if (up and down) or (left and right):
        return "STOP"

    if up:
        return "UP"

    elif down:
        return "DOWN"

    elif left:
        return "LEFT"

    elif right:
        return "RIGHT"

    else:
        return "STOP"


# Decode one complete digital Gamepad frame
def decode_packet(packet):

    if len(packet) != 8:
        return None

    if packet[0] != START_FRAME:
        return None

    if packet[1] != GAMEPAD_ID:
        return None

    if packet[2] != DIGITAL_MODE:
        return None

    if packet[3] != 0x01 or packet[4] != 0x02:
        return None

    if packet[7] != END_FRAME:
        return None

    # Byte 6 contains the directional button states
    buttons = packet[6]

    up = bool(buttons & 0x01)
    down = bool(buttons & 0x02)
    left = bool(buttons & 0x04)
    right = bool(buttons & 0x08)

    return decode_buttons(up, down, left, right)


# Test simulated Dabble Bluetooth packets
def test_decoder():

    print("Dabble Bluetooth Packet Decoder")
    print("--------------------------------")

    test_packets = [
        bytes.fromhex("FF 01 01 01 02 00 01 00"),  # UP
        bytes.fromhex("FF 01 01 01 02 00 02 00"),  # DOWN
        bytes.fromhex("FF 01 01 01 02 00 04 00"),  # LEFT
        bytes.fromhex("FF 01 01 01 02 00 08 00"),  # RIGHT
        bytes.fromhex("FF 01 01 01 02 00 00 00"),  # STOP
        bytes.fromhex("FF 01 01 01 02 00 03 00"),  # Conflict
    ]

    for packet in test_packets:

        print("Received packet:", packet.hex(" ").upper())

        command = decode_packet(packet)

        if command is not None:
            print("Decoded command:", command)
            process_command(command)

        else:
            print("Invalid or unsupported packet")

        print("--------------------------------")


# Main program
if __name__ == "__main__":
    test_decoder()
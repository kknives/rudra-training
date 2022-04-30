#!/usr/bin/env python3

import serial
import argparse

aparser = argparse.ArgumentParser(
    description="Control motors using pySerial and Arduino"
)
aparser.add_argument(
    "serialport", metavar="s", type=str, nargs=1, help="arduino's serialport address"
)
args = aparser.parse_args()

with serial.Serial() as board:
    board.baudrate = 115200
    board.port = args.serialport[0]
    print("Enter b to stop the motor")
    board.open()
    while True:
        try:
            instr = input("wasd>")
        except EOFError:
            break
        board.write(bytes(instr, encoding="utf8"))

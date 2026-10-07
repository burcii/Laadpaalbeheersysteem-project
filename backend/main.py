#!/usr/bin/env python3


"""
This file is part of the EVBox HomeLine stand-alone project.

Written 2024 by Maarten Tromp <maarten@geekabit.nl>


Website
-------
https://www.geekabit.nl/projects/managed-ev-charger-to-stand-alone/


License
-------
CC0 (no copyright, public domain)
The person who associated a work with this deed has dedicated the work to the public domain by
waiving all of his or her rights to the work worldwide under copyright law, including all related
and neighbouring rights, to the extent allowed by law. You can copy, modify, distribute and perform
the work, even for commercial purposes, all without asking permission.
https://creativecommons.org/share-your-work/public-domain/cc0/
"""

# imports
import argparse
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from typing import Set 
from datetime import datetime
from collections import deque
from typing import Deque
import serial
import serial.rs485

# project imports
import config.config as config
import hardware.frame as frame
import hardware.packet as packet
import hardware.cb_manager as cb_manager

# globals
HANDLE = None
CAPTURE = None
MONITOR = False
OUTBOX: Deque["packet.Packet"] = deque()
CB_MANAGER = cb_manager.CP(OUTBOX)


def send(p):
    """
    Send packet to charger over serial.
    """

    time.sleep(0.1)  # bus must be idle for at least 100mS
    print(f"\033[34msending\033[0m {datetime.now()}")
    data = frame.Frame(p).get_bytes()  # prints packet
    HANDLE.write(data)
    HANDLE.flush()
    if CAPTURE:
        CAPTURE.write(f"#sending {datetime.now()}\n")
        CAPTURE.write(f"{data.hex(' ').upper()}\n")
        CAPTURE.flush()


def find_frames(data):
    """
    Find any frames in data.
    """

    while True:
        # print(f"data: {data}")

        n = data.find(b"\x02")
        if n < 0:
            print(f"start of frame marker not found in data: {data}")
            return bytes()
        if n > 0:
            print(f"data found before start of frame marker: {data[:n]}")
            data = data[n:]

        m = data.find(b"\x03\xFF")
        if m < 0:
            # print("end of frame marker not found in data")
            return data

        frame_data = data[:m + 2]
        # print(f"frame data: {frame_data}")
        try:
            p = frame.Frame(frame_data).get_packet()  # prints packet
        except ValueError as error:
            print(f"ERROR: {error}")
            print(flush=True)
        else:
            if HANDLE and not MONITOR:
                CB_MANAGER.respond(p)
                while OUTBOX:
                    response = OUTBOX.pop()
                    send(response)
        finally:
            data = data[m + 2:]
        if len(data) == 0:
            return bytes()


def read_from_serial(serial_device):
    """
    Read data from charger.
    """

    data = bytes()

    global HANDLE
    HANDLE = serial.rs485.RS485(port=serial_device, baudrate=38400, timeout=0)
    print("Reading from serial port: {serial_device}.")
    print("Press ^C to stop.")

    while True:
        if HANDLE.in_waiting:
            print(f"\033[31mreceived\033[0m {datetime.now()}")
            # there is data in the serial port buffer
            new_data = HANDLE.read(HANDLE.in_waiting)
            if CAPTURE:
                CAPTURE.write(f"#received {datetime.now()}\n")
                CAPTURE.write(f"{new_data.hex(' ').upper()}\n")
                CAPTURE.flush()
            data += new_data
            data = find_frames(data)
        time.sleep(0.01)
        if HANDLE and not MONITOR:
            CB_MANAGER.timers()
            while OUTBOX:
                p = OUTBOX.pop()
                send(p)


def read_from_file(filename):
    """
    Read captured data from file.
    """

    print(f"Reading captured data from file: {filename}")
    data = bytes()
    with open(filename, mode="rt", encoding="ascii") as f:
        for line in f.readlines():
            if line[0] == "#":
                # comment
                print(line, end="")
            else:
                new_data = bytes.fromhex(line)
                # print(f"read: {new_data.hex(' ').upper()}")
                data += new_data
                data = find_frames(data)


def main():
    """
    Main function, parse command-line parameters.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--monitor", action="store_true", help="Monitor bus traffic only, do not send any messages.)")
    parser.add_argument("--capture", help="Capture bus traffic to file.")
    parser.add_argument("--replay", help="Replay captured data from file instead of live bus data.)")
    args = parser.parse_args()

    if args.capture:
        print(f"Capturing bus data to file: {args.capture}")
        global CAPTURE
        CAPTURE = open(args.capture, mode="at", encoding="ascii")

    if args.monitor:
        print("Monitoring bus")
        global MONITOR
        MONITOR = True

    if args.replay:
        read_from_file(args.replay)
    else:
        read_from_serial(config.serial_device)


app = FastAPI()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws/chargers")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == '__main__':
    main()

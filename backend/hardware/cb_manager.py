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
import datetime
from typing import Deque
# from main import manager
import asyncio

# project imports
from database import Database
import config
import hardware.packet as packet
import sched, time


class CP:
    """
    Manage a single ChargeBox charger module.
    """

    def __init__(self, outbox: Deque):
        """
        Parameters
        ----------
        outbox: packet send queue
        """

        self._outbox = outbox
        self._charger_state = 0
        self.meter_type = "01"
        self.last_update = datetime.datetime.now()

        # send first request
        request = packet.Packet()
        request.dst = packet.ADDR_BROADCAST
        request.src = packet.ADDR_CP
        request.cmd = 0x1E  # restart registration
        request.dat = ""
        self._last_message = request
        self._last_message_timestamp = datetime.datetime.now()
        self._check_message_response = False
        self._send(request)        

    def respond(self, message):
        """
        Respond to message as if you were a ChargePoint.
        """

        # TODO: create proper state machine

        if message.dst not in (packet.ADDR_BROADCAST, packet.ADDR_CP):
            print("message not meant for me")
            return

        length = len(message.dat)

        if message.cmd == 0x11:  # request for address
            if length != 15:
                print("invalid message length")
                return
            response = packet.Packet()
            response.dst = message.src
            response.src = packet.ADDR_CP
            response.cmd = message.cmd
            serial = message.dat[0:7]
            firmware_version = message.dat[7:11]  # Expected value: 0125
            hardware_generation = message.dat[13:15]  # Expected value: 03

            with Database() as db:
                db.execute_query("SELECT * FROM EVBoxes WHERE serialNumber = %s", (serial,))
                print(f"Checking if {serial} is known")
                db.fetch_results()
                if db.row_count() == 0:
                    db.execute_query(
                        "INSERT INTO EVBoxes (locationID, serialNumber, softwareVersion) VALUES (%s, %s, %s)",
                        (1, serial, firmware_version))
                    db.commit()

                db.execute_query("SELECT * FROM EVBoxes WHERE serialNumber = %s", (serial,))
                data = db.fetch_one()
                if db.row_count() != 0:
                    packet.ADDR_CHARGER = data['EVBOXID']

            response.dat = f"{serial}{packet.ADDR_CHARGER:02X}03"  # new address
            self._send(response)
            self._charger_state = 1

        elif message.cmd == 0x13:  # get meter info
            if length not in (4, 64):  # length is either 64 (ack) or 4 (nack)
                print("invalid message length")
                return
            self._disable_response_check()

        elif message.cmd == 0x21:  # heartbeat
            if length != 0:
                print("invalid message length")
                return
            response = packet.Packet()
            response.dst = message.src
            response.src = packet.ADDR_CP
            response.cmd = message.cmd
            response.dat = ""
            self._send(response)

        elif message.cmd == 0x22:  # authentication request
            if length != 26:
                print("invalid message length")
                return
            response = packet.Packet()
            response.dst = message.src
            response.src = packet.ADDR_CP
            response.cmd = message.cmd
            card_number_length = int.from_bytes(bytes.fromhex(message.dat[2:4]))
            card_number = message.dat[4:4 + card_number_length]
            status = "12"  # access denied
            if card_number == "000000AS":  # auto start
                status = "01"  # access granted
            elif card_number in config.allowed_cards:
                status = "01"  # access granted
            response.dat = f"{status}{card_number_length:02X}{card_number:022}FFFF"
            self._send(response)

        elif message.cmd == 0x23:  # metering start
            if length != 32:
                print("invalid message length")
                return
            response = packet.Packet()
            response.dst = message.src
            response.src = packet.ADDR_CP
            response.cmd = message.cmd
            session = 0
            response.dat = f"01{session:08X}{self._timestamp()}"
            self._send(response)
        # second response is never sent. Does not seem to be a problem.

        elif message.cmd == 0x24:  # metering end
            if length != 50:
                print("invalid message length")
                return
            response = packet.Packet()
            response.dst = message.src
            response.src = packet.ADDR_CP
            response.cmd = message.cmd
            response.dat = "01"
            self._send(response)

        elif message.cmd == 0x26:  # state update
            if length != 132:
                print("invalid message length")
                return
            # State order: 02 (available) → 47 (charging cable connected) → 4A (ready) → 48 (charging) → 4A (ready) → 4B (finished) → 02 (available)
            status_list = {"02": "Available", "47": "Cable Connected", "4A": "Ready", "48": "Charging", "4B": "Finished", "0A": "Error"}
            status = status_list[message.dat[0:2]]

            response = packet.Packet()
            response.dst = message.src
            response.src = packet.ADDR_CP
            response.cmd = message.cmd

            session = 0

            with Database() as db:
                db.execute_query("UPDATE EVBoxes SET status = %s WHERE EVBOXID = %s", (status, message.src))
                db.commit()

                # asyncio.create_task(manager.broadcast({
                #     "type": "status_update",
                #     "evboxId": message.src,
                #     "status": status,
                #     "timestamp": datetime.datetime.now().isoformat()
                # }))

                if (status == "Charging"):
                    # Start charging session
                    db.execute_query("INSERT INTO chargeSessions (cardUID, EVBOXID) VALUES (%s, %s)", ("04BA2A2ADA1790", message.src))
                    db.commit()

                    db.execute_query("SELECT LAST_INSERT_ID() AS sessionID")
                    result = db.fetch_one()
                    if db.row_count() > 0:
                        session = result['sessionID']
                
                else:
                    # Get charging sessions
                    db.execute_query("SELECT * FROM chargeSessions WHERE EVBOXID = %s AND status = %s", (message.src, "active"))

                    if (db.row_count() > 0):
                        session_data = db.fetch_one()
                        db.execute_query("UPDATE chargeSessions SET sessionEnd = %s, status = %s, energyUsage = 10, totalCost = 10 WHERE sessionID = %s", (datetime.datetime.now(), "completed", session_data['sessionID']))
                        db.commit()

            response.dat = f"{session:08X}{self._timestamp()}"
            self._send(response)

        elif message.cmd == 0x31:  # remote start
            if length != 2:
                print("invalid message length")
                return
            self._disable_response_check()

        elif message.cmd == 0x32:  # remote stop
            if length != 2:
                print("invalid message length")
                return
            self._disable_response_check()

        elif message.cmd == 0x33:  # get configuration
            if length not in (74, 78):  # not sure why one board sends longer response than the others
                print("invalid message length")
                return
            elif message.dat[30:32] == "00":
                self.meter_type = "00"
            self._disable_response_check()

        elif message.cmd == 0x34:  # set configuration
            if length != 4:
                print("invalid message length")
                return
            self._disable_response_check()

        elif message.cmd == 0x36:  # unknown
            if length != 2:
                print("invalid message length")
                return

        elif message.cmd == 0x37:  # unknown
            if length != 2:
                print("invalid message length")
                return

        elif message.cmd == 0x38:  # unknown
            if length != 2:
                print("invalid message length")
                return

        elif message.cmd == 0x41:  # unknown
            if length != 54:
                print("invalid message length")
                return

        elif message.cmd == 0x42:  # set serial number
            if length != 7:
                print("invalid message length")
                return

        elif message.cmd == 0x43:  # hardware info
            if length != 18:
                print("invalid message length")
                return

        elif message.cmd == 0x66:  # meter value
            if length != 44:
                print("invalid message length")
                return
            response = packet.Packet()
            response.dst = message.src
            response.src = packet.ADDR_CP
            response.cmd = message.cmd
            response.dat = ""
            self._send(response)

        elif message.cmd == 0x6A:  # charging mode
            if length != 4:
                print("invalid message length")
                return
            response = packet.Packet()
            response.dst = message.src
            response.src = packet.ADDR_CP
            response.cmd = message.cmd
            response.dat = "AA00"  # ack
            self._send(response)
            state = message.dat[0:2]
            if state == "A7":  # starting
                request = packet.Packet()
                request.dst = message.src
                request.src = packet.ADDR_CP
                request.cmd = 0x6B  # set current limit
                current_min = "003C"  # 6.0A
                current1 = "003C"
                current2 = "003C"
                current3 = "003C"
                request.dat = f"01{current_min}{current1}{current2}{current3}"
                self._send(request, True)
            elif state == "81":  # started
                request = packet.Packet()
                request.dst = message.src
                request.src = packet.ADDR_CP
                request.cmd = 0x6B  # set current limit
                current_min = "003C"  # 6.0A
                current1 = "00A0"  # 16.0A
                current2 = "00A0"
                current3 = "00A0"
                request.dat = f"01{current_min}{current1}{current2}{current3}"
                self._send(request, True)

        elif message.cmd == 0x6B:  # charging mode
            if length != 0:
                print("invalid message length")
                return
            self._disable_response_check()

        elif message.cmd == 0x6C:  # unknown
            if length != 2:
                print("invalid message length")
                return

        else:
            print("unknown message")

    def timers(self):
        """
        Handle time-sensitive messages
        """

        if self._check_message_response:
            self._check_response()

        if self._charger_state > 0:
            self._configure_charger()

    def _check_response(self):
        """
        See if a response is overdue. If so, resend last message.
        """

        if self._last_message_timestamp + datetime.timedelta(seconds=2) > datetime.datetime.now():
            return
        self._send(self._last_message, True)

    def _disable_response_check(self):
        """
        Stop checking for a response.
        """

        self._check_message_response = False

    def _configure_charger(self):
        """
        State machine for proper initialization of charger.
        """
        if self._last_message_timestamp + datetime.timedelta(seconds=5) > datetime.datetime.now():
            return

        # poor mans state machine
        if self._charger_state == 1:
            request = packet.Packet()
            request.dst = packet.ADDR_CHARGER
            request.src = packet.ADDR_CP
            request.cmd = 0x1B  # connection state changed
            heartbeat_interval = "00038400"  # 15 min
            led_enable = "00"
            request.dat = f"{heartbeat_interval}{led_enable}"
            self._send(request)
            self._charger_state = 2
        elif self._charger_state == 2:
            request = packet.Packet()
            request.dst = packet.ADDR_CHARGER
            request.src = packet.ADDR_CP
            request.cmd = 0x33  # get configuration
            request.dat = ""
            self._send(request, True)
            self._charger_state = 3
        elif self._charger_state == 3:
            request = packet.Packet()
            request.dst = packet.ADDR_CHARGER
            request.src = packet.ADDR_CP
            request.cmd = 0x34  # set configuration
            mask = "FFFFFFFF"
            led_brightness = "1E"  # 30%
            # meter_type = "01"  # "00" for pulse, "01" for serial
            auto_start = "01"
            meter_update_interval = "00000384"  # 15 min
            remote_start = "00"
            request.dat = f"{mask}{led_brightness}030000{self.meter_type}01000100000000000000{auto_start}000000003C00000384{meter_update_interval}01000000{remote_start}03E8010000"
            self._send(request, True)
            self._charger_state = 4
        elif self._charger_state == 4:
            request = packet.Packet()
            request.dst = packet.ADDR_CHARGER
            request.src = packet.ADDR_CP
            request.cmd = 0x13  # get meter info
            request.dat = ""
            self._send(request, True)
            self._charger_state = 0

    def _send(self, p, check_response=False):
        """
        Queue message for sending, handle response check.
        """

        if check_response:
            self._check_message_response = True
            self._last_message = p
        self._last_message_timestamp = datetime.datetime.now()
        self._outbox.appendleft(p)

    def _timestamp(self):
        """
        Returns current time as string
        seconds since 1 jan 2000
        """

        t = int((datetime.datetime.now() - datetime.datetime(year=2000, month=1, day=1)).total_seconds())
        return f"{t:08X}"

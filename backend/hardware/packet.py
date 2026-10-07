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
import re
from datetime import datetime, timedelta

# constants
ADDR_NEW = 0x01  # charger after bootup
ADDR_CHARGER = 0x01
ADDR_CP = 0x80
ADDR_BROADCAST = 0xBC
ADDR_CHARGESTATION = 0xFD


class Packet:
    """
    This class holds Packets of data.
    """

    def __init__(self):
        self.dst = 0
        self.src = 0
        self.cmd = 0
        self.dat = ""

    def from_payload(self, payload):
        """
        Import Packet data from Frame payload as bytes.
        No need to validate, that's already handled in the Frame class.
        """

        # decode payload
        data = payload.decode("ascii")

        # set variables
        self.dst = int.from_bytes(bytes.fromhex(data[0:2]))
        self.src = int.from_bytes(bytes.fromhex(data[2:4]))
        self.cmd = int.from_bytes(bytes.fromhex(data[4:6]))
        self.dat = data[6:]

        self._print()

        return self

    def get_payload(self):
        """
        Return Packet data as Frame payload as bytes.
        No need to validate, that's already handled in the Frame class.
        """

        payload = f"{self.dst:02X}"
        payload += f"{self.src:02X}"
        payload += f"{self.cmd:02X}"
        payload += self.dat

        # encode
        payload = payload.encode("ascii")

        self._print()

        return payload

    def _print(self):
        """
        Display Packet data.
        """

        # print(f"raw dat: {self.dat}")

        error = ""
        dst_name = self._translate_address(self.dst)
        src_name = self._translate_address(self.src)
        cmd_type = "unknown"
        cmd_name = "unknown"
        dat_name = "unknown"
        length = len(self.dat)

        foo = int.from_bytes(bytes.fromhex(self.dat[0:4]))
        if foo == 0xAA00:
            dat_name = "ack"
        elif foo == 0x0055:
            dat_name = "nack"

        if self.cmd == 0x11:
            cmd_name = "register"
            if self.dst == ADDR_CP:
                cmd_type = "request"
                if length != 15:
                    error += f"Invalid message length: {length}, expected: 15\n"
                serial = self.dat[0:7]
                firmware_version = self.dat[7:11]
                hardware_generation = self.dat[13:15]
                dat_name = f"serial number: {serial}, firmware version: {firmware_version}, hardware generation: {hardware_generation}"
            else:
                cmd_type = "response"
                if length != 11:
                    error += f"Invalid message length: {length}, expected: 11\n"
                serial = self.dat[0:7]
                gen = self.dat[9:11]
                dat_name = f"serial number: {serial}, address: {ADDR_CHARGER}, gen: {gen}"
        elif self.cmd == 0x13:
            cmd_name = "get meter info"
            if self.src == ADDR_CP:
                cmd_type = "request"
                if length != 0:
                    error += f"Invalid message length: {length}, expected: 0\n"
            else:
                cmd_type = "response"
                if length < 4:
                    error += f"Invalid message length: {length}, expected: >= 4\n"
                state = int.from_bytes(bytes.fromhex(self.dat[0:4]))
                if state == 0xAA00:
                    if length != 64:
                        error += f"Invalid message length: {length}, expected: 64\n"
                    version_number_length = int.from_bytes(bytes.fromhex(self.dat[4:6]))  # hardware or firmware version
                    version_number = self.dat[6:6 + version_number_length]
                    model_name_length = int.from_bytes(bytes.fromhex(self.dat[22:24]))
                    model_name = self.dat[24:24 + model_name_length]
                    serial_number = self.dat[40:56]
                    mains_frequency = int.from_bytes(bytes.fromhex(self.dat[56:60])) / 100
                    dat_name = f"version number: {version_number}, model name: {model_name}, serial number: {serial_number}, mains frequency: {mains_frequency}Hz"
                elif state == 0x0055:
                    if length != 4:
                        error += f"Invalid message length: {length}, expected: 4\n"
                    dat_name = "meter not found"
                else:
                    error += f"Invalid state: {state:04X}\n"
        elif self.cmd == 0x18:
            cmd_name = "request update"
            if self.src == ADDR_CP:
                cmd_type = "request"
                if length != 2:
                    error += f"Invalid message length: {length}, expected: 2\n"
                update_type = int.from_bytes(bytes.fromhex(self.dat[0:2]))
                dat_name = f"update type: {update_type}"
            else:
                error += "Invalid message: command 18 does not have response\n"
        elif self.cmd == 0x1B:
            cmd_name = "connection state changed"
            if self.src == ADDR_CP:
                cmd_type = "request"
                if length != 10:
                    error += f"Invalid message length: {length}, expected: 10\n"
                dat_name = ""
            else:
                error += "Invalid message: command 1B does not have response\n"
        elif self.cmd == 0x1C:
            cmd_name = "led ring enable"
            if self.src == ADDR_CP:
                cmd_type = "request"
                if length != 2:
                    error += f"Invalid message length: {length}, expected: 2\n"
                state = int.from_bytes(bytes.fromhex(self.dat[0:2]))
                if state == 0x00:
                    state_name = "disable"
                elif state == 0x01:
                    state_name = "enable"
                else:
                    state_name = f"invalid: {state:02X}"
                dat_name = f"state: {state_name}"
            else:
                error += "Invalid message: command 1C does not have response\n"
        elif self.cmd == 0x1E:
            cmd_name = "restart registration"
            if self.src == ADDR_CP:
                cmd_type = "request"
                if length != 0:
                    error += f"Invalid message length: {length}, expected: 0\n"
                dat_name = ""
            else:
                error += "Invalid message: command 1E does not have response\n"
        elif self.cmd == 0x21:
            cmd_name = "heartbeat"
            if self.dst == ADDR_CP:
                cmd_type = "request"
                if length != 0:
                    error += f"Invalid message length: {length}, expected: 0\n"
                dat_name = ""
            else:
                cmd_type = "response"
                if length != 0:
                    error += f"Invalid message length: {length}, expected: 0\n"
                dat_name = ""
        elif self.cmd == 0x22:
            cmd_name = "authentication request"
            if self.dst == ADDR_CP:
                cmd_type = "request"
                if length != 26:
                    error += f"Invalid message length: {length}, expected: 26\n"
            else:
                cmd_type = "response"
                if length != 30:
                    error += f"Invalid message length: {length}, expected: 30\n"
            state = int.from_bytes(bytes.fromhex(self.dat[0:2]))
            if state == 0x00:
                state_name = "authentication request"
            elif state == 0x01:
                state_name = "access granted"
            elif state == 0x03:
                state_name = "not connected to backend"
            elif state == 0x12:
                state_name = "access denied"
            elif state == 0x1D:
                state_name = "invalid card number"
            else:
                state_name = f"invalid: {state:02X}"
            dat_name = f"state: {state_name}"
            card_number_length = int.from_bytes(bytes.fromhex(self.dat[2:4]))
            if card_number_length > 0:
                card_number = self.dat[4:4 + card_number_length]
                if card_number == "000000AS":
                    dat_name += ", auto start"
                else:
                    dat_name += f", card number: {card_number}"
        elif self.cmd == 0x23:
            cmd_name = "metering start"
            if self.dst == ADDR_CP:
                cmd_type = "request"
                if length != 32:
                    error += f"Invalid message length: {length}, expected: 32\n"
                card_number_length = int.from_bytes(bytes.fromhex(self.dat[0:2]))
                card_number = self.dat[2:2 + card_number_length]
                meter_value = int.from_bytes(bytes.fromhex(self.dat[24:32])) / 1000
                dat_name = f"card number: {card_number}, meter value: {meter_value}kWh"
            else:
                cmd_type = "response"
                if length != 18:
                    error += f"Invalid message length: {length}, expected: 18\n"
                session = int.from_bytes(bytes.fromhex(self.dat[2:10]))
                timestamp = int.from_bytes(bytes.fromhex(self.dat[10:18]))
                timestamp_name = f"{datetime(year=2000, month=1, day=1) + timedelta(seconds=timestamp)}"
        elif self.cmd == 0x24:
            cmd_name = "metering end"
            if self.dst == ADDR_CP:
                cmd_type = "request"
                if length != 50:
                    error += f"Invalid message length: {length}, expected: 50\n"
                card_number_length = int.from_bytes(bytes.fromhex(self.dat[0:2]))
                card_number = self.dat[2:2 + card_number_length]
                session = int.from_bytes(bytes.fromhex(self.dat[32:40]))
                timestamp = int.from_bytes(bytes.fromhex(self.dat[42:50]))
                timestamp_name = f"{datetime(year=2000, month=1, day=1) + timedelta(seconds=timestamp)}"
                meter_value = int.from_bytes(bytes.fromhex(self.dat[24:32])) / 1000
                dat_name = f"card number: {card_number}, meter value: {meter_value}kWh, session: {session}, timestamp: {timestamp_name}"
            else:
                cmd_type = "response"
                if length != 2:
                    error += f"Invalid message length: {length}, expected: 2\n"
                dat_name = ""
        elif self.cmd == 0x26:
            cmd_name = "charger state update"
            if self.dst == ADDR_CP:
                cmd_type = "request"
                if length != 132:
                    error += f"Invalid message length: {length}, expected: 132\n"
                state = int.from_bytes(bytes.fromhex(self.dat[0:2]))
                # 02 (available) â†’ 47 (charging cable connected) â†’ 4A (ready) â†’ 48 (charging) â†’ 4A (ready) â†’ 4B (finished) â†’ 02 (available)
                if state == 0x02:
                    state_name = "available"
                elif state == 0x0A:
                    state_name = "error"
                elif state == 0x47:
                    state_name = "charging cable connected"
                elif state == 0x48:
                    state_name = "charging"
                elif state == 0x4A:
                    state_name = "ready"
                elif state == 0x4B:
                    state_name = "finished"
                else:
                    state_name = f"invalid: {state:02X}"
                #
                is_charging = int.from_bytes(bytes.fromhex(self.dat[6:8]))
                led_colour = int.from_bytes(bytes.fromhex(self.dat[8:10]))
                if led_colour == 0:
                    led_colour_name = "off"
                elif led_colour == 1:
                    led_colour_name = "green"
                elif led_colour == 2:
                    led_colour_name = "red"  # guess
                elif led_colour == 3:
                    led_colour_name = "yellow"
                elif led_colour == 4:
                    led_colour_name = "blue"
                elif led_colour == 5:
                    led_colour_name = "FIXME"  # value observed, colour unknown
                else:
                    led_colour_name = led_colour
                is_locked = int.from_bytes(bytes.fromhex(self.dat[10:12]))
                cable_current = int.from_bytes(bytes.fromhex(self.dat[12:14]))
                #
                meter_value = int.from_bytes(bytes.fromhex(self.dat[18:26])) / 1000
                #
                yet_another_status = int.from_bytes(bytes.fromhex(self.dat[30:32]))
                #
                chassis_temperature = int.from_bytes(bytes.fromhex(self.dat[52:56])) / 10
                #
                session = int.from_bytes(bytes.fromhex(self.dat[58:66]))
                #
                voltage1 = int.from_bytes(bytes.fromhex(self.dat[68:72]))
                voltage2 = int.from_bytes(bytes.fromhex(self.dat[72:76]))
                voltage3 = int.from_bytes(bytes.fromhex(self.dat[76:80]))
                current1 = int.from_bytes(bytes.fromhex(self.dat[80:84])) / 100
                current2 = int.from_bytes(bytes.fromhex(self.dat[84:88])) / 100
                current3 = int.from_bytes(bytes.fromhex(self.dat[88:92])) / 100
                socket_temperature = int.from_bytes(bytes.fromhex(self.dat[92:96]))
                power_factor1 = int.from_bytes(bytes.fromhex(self.dat[96:100])) / 1000
                power_factor2 = int.from_bytes(bytes.fromhex(self.dat[100:104])) / 1000
                power_factor3 = int.from_bytes(bytes.fromhex(self.dat[104:108])) / 1000
                current_limit = int.from_bytes(bytes.fromhex(self.dat[124:128])) / 10
                frequency = int.from_bytes(bytes.fromhex(self.dat[128:132])) / 100  # line frequency, mains frequency
                dat_name = f"state: {state_name}, is charging: {is_charging}, led colour: {led_colour_name}, is locked: {is_locked}, cable current: {cable_current}A, meter value: {meter_value}kWh, temperature: {chassis_temperature}/{socket_temperature}Â°C, session: {session}, voltage: {voltage1}/{voltage2}/{voltage3}V, current: {current1}/{current2}/{current3}A, power factor: {power_factor1}/{power_factor2}/{power_factor3}, current limit: {current_limit}A, frequency: {frequency}Hz"
            else:
                cmd_type = "response"
                if length != 16:
                    error += f"Invalid message length: {length}, expected: 16\n"
                session = int.from_bytes(bytes.fromhex(self.dat[0:8]))
                timestamp = int.from_bytes(bytes.fromhex(self.dat[8:16]))
                if timestamp == 0:
                    dat_name = "not connected to backend"
                else:
                    timestamp_name = f"{datetime(year=2000, month=1, day=1) + timedelta(seconds=timestamp)}"
                    dat_name = f"session: {session}, timestamp: {timestamp_name}"
        elif self.cmd == 0x2A:
            cmd_name = "unknown 2A"
            if self.dst == ADDR_CP:
                cmd_type = "request"
                dat_name = ""
            else:
                cmd_type = "response"
                dat_name = ""
        elif self.cmd == 0x31:
            cmd_name = "remote start"
            if self.src == ADDR_CP:
                cmd_type = "request"
                if length != 24:
                    error += f"Invalid message length: {length}, expected: 24\n"
                card_number_length = int.from_bytes(bytes.fromhex(self.dat[0:2]))
                card_number = self.dat[2:2 + card_number_length]
                dat_name = f"card number: {card_number}"
            else:
                cmd_type = "response"
                if length != 2:
                    error += f"Invalid message length: {length}, expected: 2\n"
                state = int.from_bytes(bytes.fromhex(self.dat[0:2]))
                if state == 0x01:
                    state_name = "success"
                elif state == 0x23:
                    state_name = "failed"
                else:
                    state_name = f"invalid: {state:02X}"
                dat_name = f"state: {state_name}"
        elif self.cmd == 0x32:
            cmd_name = "remote stop"
            if self.src == ADDR_CP:
                cmd_type = "request"
                if length != 8:
                    error += f"Invalid message length: {length}, expected: 8\n"
                session = int.from_bytes(bytes.fromhex(self.dat[0:8]))
                dat_name = f"session: {session}"
            else:
                cmd_type = "response"
                if length != 2:
                    error += f"Invalid message length: {length}, expected: 2\n"
                state = int.from_bytes(bytes.fromhex(self.dat[0:2]))
                if state == 0x1:
                    state_name = "success"
                elif state == 0x23:
                    state_name = "failed"
                else:
                    state_name = f"invalid: {state:02X}"
                dat_name = f"state: {state_name}"
        elif self.cmd == 0x33:
            cmd_name = "get configuration"
            if self.src == ADDR_CP:
                cmd_type = "request"
                if length != 0:
                    error += f"Invalid message length: {length}, expected: 0\n"
                dat_name = ""
            else:
                cmd_type = "response"
                if length not in (74, 78):  # not sure why one board sends longer response than the others
                    error += f"Invalid message length: {length}, expected: 74\n"
                #
                meter_update_interval = int.from_bytes(bytes.fromhex(self.dat[20:24]))
                #
                meter_type = int.from_bytes(bytes.fromhex(self.dat[30:32]))
                if meter_type == 0:
                    meter_type_name = "pulse"
                elif meter_type == 1:
                    meter_type_name = "serial"
                else:
                    meter_type_name = "invalid"
                #
                led_brightness = int.from_bytes(bytes.fromhex(self.dat[36:38]))
                #
                auto_start = int.from_bytes(bytes.fromhex(self.dat[54:56]))
                #
                remote_start = int.from_bytes(bytes.fromhex(self.dat[66:68]))
                #
                dat_name = f"led brightness: {led_brightness}%, meter update interval: {meter_update_interval}s, meter type: {meter_type_name}, auto start: {auto_start}, remote start: {remote_start}"
        elif self.cmd == 0x34:
            cmd_name = "set configuration"
            if self.src == ADDR_CP:
                cmd_type = "request"
                if length != 86:
                    error += f"Invalid message length: {length}, expected: 86\n"
                #
                led_brightness = int.from_bytes(bytes.fromhex(self.dat[8:10]))
                #
                meter_type = int.from_bytes(bytes.fromhex(self.dat[16:18]))
                if meter_type == 0:
                    meter_type_name = "pulse"
                elif meter_type == 1:
                    meter_type_name = "serial"
                else:
                    meter_type_name = "invalid"
                #
                auto_start = int.from_bytes(bytes.fromhex(self.dat[38:40]))
                #
                meter_update_interval = int.from_bytes(bytes.fromhex(self.dat[58:66]))
                #
                remote_start = int.from_bytes(bytes.fromhex(self.dat[74:76]))
                #
                dat_name = f"led brightness: {led_brightness}%, meter update interval: {meter_update_interval}s, meter type: {meter_type_name}, auto start: {auto_start}, remote start: {remote_start}"
            else:
                cmd_type = "response"
                if length != 4:
                    error += f"Invalid message length: {length}, expected: 4\n"
        elif self.cmd == 0x35:
            cmd_name = "reboot"
            if self.src == ADDR_CP:
                cmd_type = "request"
                dat_name = ""
            else:
                error += "Invalid message: command 35 does not have response\n"
        elif self.cmd == 0x36:
            cmd_name = "unknown 36"
            if self.src == ADDR_CP:
                cmd_type = "request"
                dat_name = ""
            else:
                cmd_type = "response"
                dat_name = ""
        elif self.cmd == 0x37:
            cmd_name = "unknown 37"
            if self.src == ADDR_CP:
                cmd_type = "request"
                dat_name = ""
            else:
                cmd_type = "response"
                dat_name = ""
        elif self.cmd == 0x38:
            cmd_name = "unknown 38"
            if self.src == ADDR_CP:
                cmd_type = "request"
                dat_name = ""
            else:
                cmd_type = "response"
                dat_name = ""
        elif self.cmd == 0x41:
            cmd_name = "unknown 41"
            cmd_type = "unknown"  # both CP and charger can initiate
            dat_name = ""
        elif self.cmd == 0x42:
            cmd_name = "set serial number"
            if self.src == ADDR_CP:
                cmd_type = "request"
                if length != 7:
                    error += f"Invalid message length: {length}, expected: 7\n"
                serial = self.dat[0:7]
                dat_name = f"serial number: {serial}"
            else:
                cmd_type = "response"
                if length != 7:
                    error += f"Invalid message length: {length}, expected: 7\n"
                serial = self.dat[0:7]
                dat_name = f"serial number: {serial}"
        elif self.cmd == 0x43:
            cmd_name = "hardware info"
            if self.src == ADDR_CP:
                cmd_type = "request"
                if length != 0:
                    error += f"Invalid message length: {length}, expected: 0\n"
                dat_name = ""
            else:
                cmd_type = "response"
                if length != 18:
                    error += f"Invalid message length: {length}, expected: 18\n"
                hardware_generation = self.dat[0:2]
                firmware_version = self.dat[2:6]
                dat_name = f"hardware generation: {hardware_generation}, firmware version: {firmware_version}"
        elif self.cmd == 0x65:
            cmd_name = "set meter update interval"
            if self.src == ADDR_CP:
                cmd_type = "request"
                if length != 4:
                    error += f"Invalid message length: {length}, expected: 4\n"
                interval = int.from_bytes(bytes.fromhex(self.dat[0:4]))
                if interval == 0:
                    dst_name = "interval: off"
                else:
                    dat_name = f"interval: {interval}s"
            else:
                error += "Invalid message: command 65 does not have response\n"
        elif self.cmd == 0x66:
            cmd_name = "meter value"
            if self.dst == ADDR_CP:
                cmd_type = "request"
                if length != 44:
                    error += f"Invalid message length: {length}, expected: 44\n"
                voltage1 = int.from_bytes(bytes.fromhex(self.dat[0:4]))
                voltage2 = int.from_bytes(bytes.fromhex(self.dat[4:8]))
                voltage3 = int.from_bytes(bytes.fromhex(self.dat[8:12]))
                current1 = int.from_bytes(bytes.fromhex(self.dat[12:16])) / 100
                current2 = int.from_bytes(bytes.fromhex(self.dat[16:20])) / 100
                current3 = int.from_bytes(bytes.fromhex(self.dat[20:24])) / 100
                power_factor1 = int.from_bytes(bytes.fromhex(self.dat[24:28])) / 1000
                power_factor2 = int.from_bytes(bytes.fromhex(self.dat[28:32])) / 1000
                power_factor3 = int.from_bytes(bytes.fromhex(self.dat[32:36])) / 1000
                meter_value = int.from_bytes(bytes.fromhex(self.dat[36:44])) / 1000
                dat_name = f"voltage: {voltage1}/{voltage2}/{voltage3}V, current: {current1}/{current2}/{current3}A, power factor: {power_factor1}/{power_factor2}/{power_factor3}, meter value: {meter_value}kWh"
            else:
                cmd_type = "response"
                if length != 0:
                    error += f"Invalid message length: {length}, expected: 0\n"
                dat_name = ""
        elif self.cmd == 0x6A:
            cmd_name = "charging state"
            if self.dst == ADDR_CP:
                cmd_type = "request"
                if length != 4:
                    error += f"Invalid message length: {length}, expected: 4\n"
                state = int.from_bytes(bytes.fromhex(self.dat[0:2]))
                if state == 0x07:
                    state_name = "unknown 07"  # mentioned by Harm Otten
                elif state == 0x20:
                    state_name = "unknown 20"  # observed
                elif state == 0x80:
                    state_name = "unplugged"
                elif state == 0x81:
                    state_name = "charging"
                elif state == 0xA0:
                    state_name = "available"
                elif state == 0xA7:
                    state_name = "ready"
                elif state == 0xC1:
                    state_name = "finished"
                elif state == 0xE7:
                    state_name = "failed"
                else:
                    state_name = f"invalid: {state:02X}"
                dat_name = f"state: {state_name}"
            else:
                cmd_type = "response"
                if length != 4:
                    error += f"Invalid message length: {length}, expected: 4\n"
                state = int.from_bytes(bytes.fromhex(self.dat[0:4]))
                if state == 0xAA00:
                    state_name = "ack"
                else:
                    state_name = f"invalid: {state:04X}"
                dat_name = f"{state_name}"
        elif self.cmd == 0x6B:
            cmd_name = "set current limit"
            if self.src == ADDR_CP:
                cmd_type = "request"
                if length != 18:
                    error += f"Invalid message length: {length}, expected: 18\n"
                current_min = int.from_bytes(bytes.fromhex(self.dat[2:6])) / 10
                current1 = int.from_bytes(bytes.fromhex(self.dat[6:10])) / 10
                current2 = int.from_bytes(bytes.fromhex(self.dat[10:14])) / 10
                current3 = int.from_bytes(bytes.fromhex(self.dat[14:18])) / 10
                dat_name = f"current min: {current_min}A, current limit: {current1}/{current2}/{current3}A"
            else:
                cmd_type = "response"
                if length != 0:
                    error += f"Invalid message length: {length}, expected: 0\n"
                dat_name = ""
        elif self.cmd == 0x6C:
            cmd_name = "unknown 6C"
            if self.src == ADDR_CP:
                cmd_type = "request"
                dat_name = ""
            else:
                cmd_type = "response"
                dat_name = ""
        elif self.cmd == 0xE1:
            cmd_name = "unknown E1"
            if self.src == ADDR_CP:
                cmd_type = "request"
                dat_name = ""
            else:
                cmd_type = "response"
                dat_name = ""
        elif self.cmd == 0xE3:
            cmd_name = "reboot"
            if self.dst == ADDR_CP:
                cmd_type = "request"
                dat_name = ""
            else:
                cmd_type = "response"
                dat_name = ""
        elif self.cmd == 0xE4:
            cmd_name = "unknown E4"
            if self.dst == ADDR_CP:
                cmd_type = "request"
                dat_name = ""
            else:
                cmd_type = "response"
                dat_name = ""
        elif self.cmd == 0xE6:
            cmd_name = "unknown E6"
            if self.src == ADDR_CP:
                cmd_type = "request"
                dat_name = ""
            else:
                cmd_type = "response"
                dat_name = ""
        elif self.cmd == 0xEB:
            cmd_name = "unknown EB"
            if self.dst == ADDR_CP:
                cmd_type = "request"
                dat_name = ""
            else:
                cmd_type = "response"
                dat_name = ""
        elif self.cmd == 0xEC:
            cmd_name = "unknown EC"
            if self.dst == ADDR_CP:
                cmd_type = "request"
                dat_name = ""
            else:
                cmd_type = "response"
                dat_name = ""
        elif self.cmd == 0xED:
            cmd_name = "unknown ED"
            if self.src == ADDR_CP:
                cmd_type = "request"
                dat_name = ""
            else:
                cmd_type = "response"
                dat_name = ""
        elif self.cmd == 0xF0:
            cmd_name = "unknown F0"
            if self.dst == ADDR_CHARGESTATION:
                cmd_type = "response"
                dat_name = ""
            else:
                cmd_type = "request"
                dat_name = ""
        elif self.cmd == 0xF1:
            cmd_name = "unknown F1"
            if self.dst == ADDR_CHARGESTATION:
                cmd_type = "response"
                dat_name = ""
            else:
                cmd_type = "request"
                dat_name = ""
        elif self.cmd == 0xF2:
            cmd_name = "unknown F2"
            if self.dst == ADDR_CHARGESTATION:
                cmd_type = "response"
                dat_name = ""
            else:
                cmd_type = "request"
                dat_name = ""
        elif self.cmd == 0xF3:
            cmd_name = "unknown F3"
            if self.dst == ADDR_CHARGESTATION:
                cmd_type = "response"
                dat_name = ""
            else:
                cmd_type = "request"
                dat_name = ""
        elif self.cmd == 0xF4:
            cmd_name = "unknown F4"
            if self.dst == ADDR_CHARGESTATION:
                cmd_type = "response"
                dat_name = ""
            else:
                cmd_type = "request"
                dat_name = ""
        elif self.cmd == 0xF5:
            cmd_name = "unknown F5"
            if self.dst == ADDR_CHARGESTATION:
                cmd_type = "response"
                dat_name = ""
            else:
                cmd_type = "request"
                dat_name = ""
        elif self.cmd == 0xF6:
            cmd_name = "reboot"
            if self.dst == ADDR_CHARGESTATION:
                cmd_type = "response"
                dat_name = ""
            else:
                cmd_type = "request"
                dat_name = ""
        elif self.cmd == 0xF7:
            cmd_name = "unknown F7"
            if self.dst == ADDR_CHARGESTATION:
                cmd_type = "response"
                dat_name = ""
            else:
                cmd_type = "request"
                dat_name = ""
        elif self.cmd == 0xF8:
            cmd_name = "unknown F8"
            if self.dst == ADDR_CHARGESTATION:
                cmd_type = "response"
                dat_name = ""
            else:
                cmd_type = "request"
                dat_name = ""
        elif self.cmd == 0xF9:
            cmd_name = "unknown F9"
            if self.dst == ADDR_CHARGESTATION:
                cmd_type = "response"
                dat_name = ""
            else:
                cmd_type = "request"
                dat_name = ""
        elif self.cmd == 0xFA:
            cmd_name = "unknown FA"
            if self.dst == ADDR_CHARGESTATION:
                cmd_type = "response"
                dat_name = ""
            else:
                cmd_type = "request"
                dat_name = ""
        elif self.cmd == 0xFB:
            cmd_name = "unknown FB"
            if self.dst == ADDR_CHARGESTATION:
                cmd_type = "response"
                dat_name = ""
            else:
                cmd_type = "request"
                dat_name = ""
        elif self.cmd == 0xFD:
            cmd_name = "reboot"
            if self.dst == ADDR_CHARGESTATION:
                cmd_type = "response"
                dat_name = ""
            else:
                cmd_type = "request"
                dat_name = ""

        dat_fmt = self.dat
        dat_fmt = re.sub(r"(\w{4})", r"\1 ", dat_fmt).strip()  # insert space every 4 characters for readability

        print(f"src: {self.src:02X} ({src_name})")
        print(f"dst: {self.dst:02X} ({dst_name})")
        print(f"cmd: {self.cmd:02X} ({cmd_name})")
        print(f"typ: {cmd_type}")
        if length > 0:
            print(f"dat: {dat_fmt} ({dat_name}), length: {length}")
        print(flush=True)

        if error:
            raise ValueError(error)

    def _translate_address(self, address):
        """
        Resolve numeric address to name
        """

        if address == ADDR_NEW:
            name = "new"
        elif address == ADDR_CHARGER:
            name = "charger"
        elif address == ADDR_CP:
            name = "CP"
        elif address == ADDR_BROADCAST:
            name = "broadcast"
        elif address == 0xA0:
            name = "SmartGrid"
        elif address == ADDR_CHARGESTATION:
            name = "ChargeStation"
        elif address == 0x70:
            name = "unknown 70"
        else:
            name = "unknown address"
        return name

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

# project imports
from hardware.packet import Packet


class Frame:
    """
    This class holds data frames.
    """

    def __init__(self, data):
        """
        Create Frame from either bytes or Packet.
        """

        self._payload = bytes()

        if isinstance(data, bytes):
            self._from_bytes(data)
        elif isinstance(data, Packet):
            self._from_packet(data)
        else:
            raise ValueError()

    def _from_bytes(self, data):
        """
        Import Frame from bytes.
        """

        # print(f"frame: {data.hex(' ')}")
        self._validate(data)
        self._payload = data[1:-6]

    def get_bytes(self):
        """
        Return frame as bytes.
        """

        # start of frame marker
        start = b"\x02"
        data = start

        # payload
        data += self._payload

        # ckecksum
        data += self._calculate_checksum(self._payload)

        # parity
        data += self._calculate_parity(self._payload)

        # end of frame marker
        end = b"\x03\xFF"
        data += end

        # print(f"frame: {data.hex(' ')}")
        self._validate(data)
        return data

    def _from_packet(self, p):
        """
        Import Frame payload from Packet.
        """

        self._payload = p.get_payload()

        return self

    def get_packet(self):
        """
        Return Frame payload as Packet.
        """

        return Packet().from_payload(self._payload)

    def _calculate_checksum(self, payload):
        """
        Calculate frame checksum.
        """

        checksum = sum(payload) % 256
        checksum_enc = f"{checksum:02X}".encode("ascii")
        # print(f"calculated checksum: {checksum:02X}")
        return checksum_enc

    def _calculate_parity(self, payload):
        """
        Calculate frame parity.
        """

        parity = 0
        for payload_byte in payload:
            parity = parity ^ payload_byte
        parity_enc = f"{parity:02X}".encode("ascii")
        # print(f"calculated parity: {parity:02X}")
        return parity_enc

    def _validate(self, frame):
        error = ""

        # length
        length = len(frame)
        if length < 13:
            error += f"Invalid frame length: {length}, expected: >= 13\n"

        # start of frame marker
        start = frame[0:1]
        if start != b"\x02":
            error += f"Invalid start of frame marker: {start}\n"

        # end of frame marker
        end = frame[-2:]
        if end != b"\x03\xFF":
            error += f"Invalid end of frame marker: {end}\n"

        # payload
        payload = frame[1:-6]
        if b"\x02" in payload:
            error += "Start of frame marker inside payload.\n"
        if b"\x03" in payload:
            error += "End of frame marker inside payload.\n"
        for b in payload:
            # if not (0x30 <= b <= 0x39 or 0x41 <= b <= 0x5A): # 0-9, A-Z
            if not (b == 0x00 or 0x30 <= b <= 0x39 or 0x41 <= b <= 0x5A):  # null, 0-9, A-Z
                error += f"Invalid value in frame payload: {b:02X}.\n"

        # checksum
        checksum = frame[-6:-4]
        if not checksum == self._calculate_checksum(payload):
            error += "Invalid frame checksum.\n"

        # parity
        parity = frame[-4:-2]
        if not parity == self._calculate_parity(payload):
            error += "Invalid frame parity.\n"

        if error:
            error += f"Frame: {frame.hex(' ')}"
            # print(error)
            raise ValueError(error)

        return True

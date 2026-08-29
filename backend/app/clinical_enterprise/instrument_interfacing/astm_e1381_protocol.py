"""
AcuPath Enterprise LIS - ASTM E1381-02 Standard Specification
For Low-Level Serial & TCP/IP Data Link Protocol Between Laboratory Instruments and LIS.
"""

from typing import Dict, List, Optional, Tuple, Callable
import enum
import time
import logging

logger = logging.getLogger("acupath.astm.e1381")


class ASTMControlChar:
    NUL = b"\x00"
    SOH = b"\x01"
    STX = b"\x02"
    ETX = b"\x03"
    EOT = b"\x04"
    ENQ = b"\x05"
    ACK = b"\x06"
    TAB = b"\x09"
    LF  = b"\x0A"
    VT  = b"\x0B"
    FF  = b"\x0C"
    CR  = b"\x0D"
    NAK = b"\x15"
    SYN = b"\x16"
    ETB = b"\x17"


class ASTMState(enum.Enum):
    IDLE = 0
    ESTABLISHING_SESSION = 1
    RECEIVING_FRAMES = 2
    SENDING_FRAMES = 3
    TERMINATING_SESSION = 4
    ERROR_RECOVERY = 5


class ASTME1381Protocol:
    """Low-level ASTM E1381 packet framing, frame sequence verification, and checksum validation."""

    @staticmethod
    def calculate_checksum(data: bytes) -> str:
        """Calculates modulo 256 two-character hexadecimal checksum."""
        total = sum(data) % 256
        return f"{total:02X}"

    @staticmethod
    def verify_frame(frame: bytes) -> Tuple[bool, int, str]:
        """
        Validates ASTM Frame: <STX> [FrameNumber] [Data] (<ETX> | <ETB>) [CS1] [CS2] <CR> <LF>
        Returns (is_valid, frame_number, data_str)
        """
        if not frame.startswith(ASTMControlChar.STX) or not frame.endswith(ASTMControlChar.CR + ASTMControlChar.LF):
            return False, -1, ""

        if len(frame) < 7:
            return False, -1, ""

        # Extract frame number
        try:
            frame_num = int(chr(frame[1]))
        except ValueError:
            return False, -1, ""

        # Find ETX or ETB
        etx_idx = frame.rfind(ASTMControlChar.ETX)
        if etx_idx == -1:
            etx_idx = frame.rfind(ASTMControlChar.ETB)
        if etx_idx == -1:
            return False, -1, ""

        data_bytes = frame[2:etx_idx]
        checksum_bytes = frame[etx_idx + 1:etx_idx + 3]
        payload_for_cs = frame[1:etx_idx + 1]

        expected_cs = ASTME1381Protocol.calculate_checksum(payload_for_cs)
        actual_cs = checksum_bytes.decode("ascii", errors="ignore").upper()

        if expected_cs != actual_cs:
            logger.warning(f"ASTM Checksum mismatch: expected {expected_cs}, got {actual_cs}")
            return False, frame_num, ""

        return True, frame_num, data_bytes.decode("utf-8", errors="ignore")

    @staticmethod
    def format_frame(frame_number: int, data: str, is_last_frame: bool = True) -> bytes:
        """Constructs a fully framed ASTM E1381 binary packet."""
        terminator = ASTMControlChar.ETX if is_last_frame else ASTMControlChar.ETB
        fn_byte = str(frame_number % 8).encode("ascii")
        data_bytes = data.encode("utf-8")
        raw_body = fn_byte + data_bytes + terminator
        checksum = ASTME1381Protocol.calculate_checksum(raw_body).encode("ascii")
        return ASTMControlChar.STX + raw_body + checksum + ASTMControlChar.CR + ASTMControlChar.LF

"""
AcuPath Enterprise LIS - Beckman Coulter DxH 800/900 Automated Hematology System Driver
Handles TCP/IP and RS-232 serial telemetry, bi-directional query-mode, and automated result parsing.
"""

from typing import Dict, List, Optional, Any, Tuple
import datetime
import logging
from ..astm_e1381_protocol import ASTME1381Protocol, ASTMControlChar
from ..astm_e1394_parser import ASTME1394Parser, ASTMMessage

logger = logging.getLogger("acupath.driver.beckman_dxh")


class BeckmanDxHDriver:
    """Driver implementation for Beckman Coulter DxH 800/900 Automated Hematology System Driver."""

    def __init__(self, instrument_id: str = "BECKMANDXHDRIVER-01", host: str = "192.168.1.100", port: int = 5100):
        self.instrument_id = instrument_id
        self.host = host
        self.port = port
        self.is_connected = False
        self.last_heartbeat = None
        self.total_tests_processed = 0

    def parse_analyzer_payload(self, raw_frames: List[bytes]) -> Optional[ASTMMessage]:
        """Validates all incoming ASTM frames, strips transport wrappers, and reconstructs message records."""
        records: List[str] = []
        for frame in raw_frames:
            is_valid, fn, data = ASTME1381Protocol.verify_frame(frame)
            if is_valid and data:
                records.append(data)
            else:
                logger.warning(f"Frame validation failed on {self.instrument_id}")

        if not records:
            return None

        msg = ASTME1394Parser.parse_message(records)
        self.total_tests_processed += len(msg.patients)
        self.last_heartbeat = datetime.datetime.utcnow()
        return msg

    def build_query_response_order(self, sample_barcode: str, test_codes: List[str]) -> List[bytes]:
        """Constructs ASTM query response frame sequence for host-query worklist download."""
        h_rec = f"H|\\^&|||ACUPATH_LIS|||||||P|1394-97|{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        p_rec = f"P|1||{sample_barcode}|||||||||||"
        test_str = "\\".join(f"^^^{code}" for code in test_codes)
        o_rec = f"O|1|{sample_barcode}||{test_str}|R|{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}|||||N||||WHOLE_BLOOD"
        l_rec = "L|1|N"

        frames = [
            ASTME1381Protocol.format_frame(1, h_rec),
            ASTME1381Protocol.format_frame(2, p_rec),
            ASTME1381Protocol.format_frame(3, o_rec),
            ASTME1381Protocol.format_frame(4, l_rec)
        ]
        return frames

    def get_instrument_telemetry(self) -> Dict[str, Any]:
        return {
            "instrument_id": self.instrument_id,
            "status": "ONLINE" if self.is_connected else "STANDBY",
            "host": self.host,
            "port": self.port,
            "total_processed": self.total_tests_processed,
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None
        }

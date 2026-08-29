"""
AcuPath Enterprise LIS - Minimal Lower Layer Protocol (MLLP) TCP Server
Implements standard framing: <VT> (0x0B) <HL7 Message> <FS> (0x1C) <CR> (0x0D)
Allows Hospital Information Systems (HIS) and EHRs to exchange real-time TCP laboratory data.
"""

import asyncio
import logging
from typing import Callable, Optional

from .hl7_v2_parser import HL7Message, HL7Validator, HL7AckGenerator

logger = logging.getLogger("acupath.mllp")

MLLP_START_BLOCK = b"\x0b"
MLLP_END_BLOCK = b"\x1c\x0d"


class MLLPServer:
    """Asynchronous MLLP TCP Server for handling bidirectional HL7 v2 telemetry streams."""

    def __init__(self, host: str = "0.0.0.0", port: int = 2575, message_handler: Optional[Callable] = None):
        self.host = host
        self.port = port
        self.message_handler = message_handler
        self.server: Optional[asyncio.Server] = None
        self._is_running = False

    async def start(self):
        self.server = await asyncio.start_server(self._handle_client, self.host, self.port)
        self._is_running = True
        logger.info(f"MLLP Server listening on {self.host}:{self.port}")

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self._is_running = False
            logger.info("MLLP Server stopped.")

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        client_addr = writer.get_extra_info("peername")
        logger.info(f"New MLLP connection from {client_addr}")
        buffer = b""

        try:
            while self._is_running:
                chunk = await reader.read(4096)
                if not chunk:
                    break
                buffer += chunk

                while MLLP_START_BLOCK in buffer and MLLP_END_BLOCK in buffer:
                    start_idx = buffer.find(MLLP_START_BLOCK)
                    end_idx = buffer.find(MLLP_END_BLOCK, start_idx)

                    if start_idx != -1 and end_idx != -1:
                        hl7_bytes = buffer[start_idx + 1:end_idx]
                        buffer = buffer[end_idx + 2:]
                        hl7_text = hl7_bytes.decode("utf-8", errors="ignore")

                        # Parse Message
                        msg = HL7Message.from_string(hl7_text)
                        is_valid, errors = HL7Validator.validate_message(msg)

                        if is_valid:
                            ack = HL7AckGenerator.generate_ack(msg, ack_code="AA")
                            if self.message_handler:
                                await self.message_handler(msg)
                        else:
                            ack = HL7AckGenerator.generate_ack(msg, ack_code="AE", error_message="; ".join(errors))

                        # Send ACK
                        ack_payload = MLLP_START_BLOCK + ack.to_hl7().encode("utf-8") + MLLP_END_BLOCK
                        writer.write(ack_payload)
                        await writer.drain()

        except Exception as e:
            logger.error(f"Error handling MLLP client {client_addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            logger.info(f"Closed MLLP connection from {client_addr}")

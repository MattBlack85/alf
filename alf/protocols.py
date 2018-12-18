import asyncio
import logging


LOGGER = logging.getLogger('alf.protocol')
QUEUE = asyncio.Queue()


class LogServerProtocol(asyncio.Protocol):
    """
    Main protocol for ALF, whenever data is received over he socket,
    the message is put into the queue.
    """

    def connection_made(self, transport):
        """
        Set the transport for the actual connection
        """
        self.transport = transport  # pylint: disable=W0201

    def data_received(self, data):
        """
        Put data ino the queue after it's received.
        """
        LOGGER.debug(f'Received {len(data)} bytes')
        data = data.split(b'\r\n')
        for msg in data:
            if msg:
                QUEUE.put_nowait(msg)

import asyncio
import logging
import os
import signal

import psutil
from alf.protocols import LogServerProtocol, QUEUE
from alf.workers import Worker

ALF_LOGGER = logging.getLogger('alf')
ALF_LOGGER.setLevel(logging.DEBUG)
LOGGER = logging.getLogger('alf.app')
PROCESS = psutil.Process(os.getpid())


class App:
    def __init__(self, socket_path, url, *, logfile=None):
        self.protocol = LogServerProtocol
        self.worker = Worker
        self.url = url
        self.logfile = logfile or '/tmp/alf.log'
        self.init_logger_handler()
        self.loop = asyncio.get_event_loop()
        coro = self.loop.create_unix_server(LogServerProtocol, path=socket_path)
        self.server = self.loop.run_until_complete(coro)
        # Init the server to deal with shutdown
        for sig in ('SIGINT', 'SIGTERM'):
            self.loop.add_signal_handler(getattr(signal, sig),
                                         lambda: self.pre_stop())

    def init_logger_handler(self):
        handler = logging.FileHandler(self.logfile)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s - %(message)s')
        )
        ALF_LOGGER.addHandler(handler)

    def dump_statistics(self):
        LOGGER.info('CPU USAGE: %.2f | MEMORY USAGE: %.2f | QUEUED: %d',
                    PROCESS.cpu_percent(), PROCESS.memory_percent(), QUEUE.qsize())
        self.loop.call_later(60, self.dump_statistics)

    def start(self):
        LOGGER.info('Serving on {}'.format(self.server.sockets[0].getsockname()))

        worker = Worker(QUEUE, self.url)
        self.loop.create_task(worker.start())
        self.dump_statistics()
        self.loop.run_forever()
        # Shutdown the server gracefully
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        LOGGER.info('Shutdown complete, closing loop and exiting')
        self.loop.close()

    def pre_stop(self):
        LOGGER.info('Starting gracefully shutdown procedure...')
        for p in asyncio.Task.all_tasks():
            p.cancel()
        asyncio.ensure_future(self.stop())

    async def stop(self):
        self.loop.stop()

import logging
import os
import pickle

import aiohttp

LOGGER = logging.getLogger('alf.worker')


class Worker:
    """
    Basic worker to monitor for incoming messages, once a message is popped
    out of the queue, it is unpickled and then sent further via http
    """

    def __init__(self, queue, url):
        self.queue = queue
        self.url = url

    async def start(self):
        """
        Infinite loop to pop out messages from the queue and take action
        """
        async with aiohttp.ClientSession() as session:
            while True:
                msg = await self.queue.get()
                LOGGER.debug('MSG from queue: %s', msg)
                await self.send_message(session, msg)

    async def send_message(self, session, msg):
        """
        Send the actual message to a remote server
        """
        try:
            async with session.post(self.url, json=msg) as resp:
                resp = await resp.json()
                LOGGER.debug('RESPONSE: %s', resp)
        except aiohttp.client_exceptions.ClientConnectorError as exc:
            LOGGER.error(exc)

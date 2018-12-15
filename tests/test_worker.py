import asyncio

import pytest

from alf.workers import Worker


@pytest.fixture
def queue():
    return asyncio.Queue()


def test_worker_initialized_as_expected(queue):
    worker = Worker(queue, 'example.com', port=1200)

    assert worker.queue is queue
    assert worker.protocol == 'http'
    assert worker.url == 'http://example.com:1200'

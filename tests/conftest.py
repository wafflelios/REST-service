import asyncio

import pytest
from fastapi.testclient import TestClient

from src.main import app


# Из документации python-asyncio
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)

import asyncio

import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient


@pytest_asyncio.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Create a new application for testing
@pytest_asyncio.fixture(scope="session")
def app() -> FastAPI:
    from math_api.main import app

    return app


# Make requests in our tests
@pytest_asyncio.fixture(scope="session")
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
            trust_env=False,
        ) as client:
            yield client

import json

import pytest
from starlette.status import HTTP_200_OK

#simple tests for demonstration

@pytest.mark.asyncio
async def test_example_test_case(client):
    response = await client.get("/health")
    print(response.content)
    assert response.status_code == HTTP_200_OK


@pytest.mark.asyncio
async def test_add(client):
    response = await client.get("/add", params={"x": 1000, "y": 1001})
    assert response.status_code == HTTP_200_OK
    content = json.loads(response.content)
    assert content["answer"] == 2001.0


@pytest.mark.asyncio
async def test_subtract(client):
    response = await client.get("/subtract", params={"x": 1000, "y": 1001})
    assert response.status_code == HTTP_200_OK
    content = json.loads(response.content)
    assert content["answer"] == -1.0


@pytest.mark.asyncio
async def test_divide(client):
    response = await client.get("/divide", params={"x": 10, "y": 2})
    assert response.status_code == HTTP_200_OK
    content = json.loads(response.content)
    assert content["answer"] == 5.0


@pytest.mark.asyncio
async def test_multiply(client):
    response = await client.get("/multiply", params={"x": 5, "y": 5})
    assert response.status_code == HTTP_200_OK
    content = json.loads(response.content)
    assert content["answer"] == 25.0

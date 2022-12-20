from fastapi import status
from httpx import AsyncClient
import pytest

from app.core.stream import RedisClient


@pytest.mark.parametrize("recording", [
    {"vehicle_id": "1", "signals": {"speed_kmh": 100}},
    {"vehicle_id": "1", "signals": {}},
])
async def test_record_signal(recording: dict, client: AsyncClient):
    response = await client.post("/record-signal/", json=recording)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": f"Vehicle {recording['vehicle_id']} was recorded!"}


@pytest.mark.parametrize('recording', [
    {"vehicle_id": {"id": "1"}, "signals": "speed"},
    {"vehicle_id": "1", "signals": "speed"},
    {"vehicle_id": {"id": "1"}, "signals": {"speed_kmh": 100}},
])
async def test_record_signal_with_incorrect_data(recording: dict, client: AsyncClient):
    response = await client.post("/record-signal/", json=recording)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_vehicles(client: AsyncClient, redis_test: RedisClient):
    await redis_test.set_item('some', 'value')

    response = await client.get("/vehicles/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == ['some']

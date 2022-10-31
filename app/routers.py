import logging

from app.core.models import Recording
from app.core.settings import get_redis_client
from app.core.settings import VEHICLE_CHANNEL
from app.core.settings import VEHICLE_CHANNELS
from app.core.stream import RedisClient
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from redis.exceptions import ConnectionError
from redis.exceptions import DataError
from redis.exceptions import PubSubError


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post('/record-signal/', status_code=status.HTTP_201_CREATED, description='Record vehicle signals')
async def record_signal(recording: Recording, redis_client: RedisClient = Depends(get_redis_client)):
    name = VEHICLE_CHANNEL.format(recording.vehicle_id)
    try:
        await redis_client.publish(channel=name, data=recording.signals)
        await redis_client.set_item(name=name, value=recording.vehicle_id)
    except (PubSubError, ConnectionError, DataError) as error:
        logger.error(error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Service is unavailable!',
        )
    return {'message': f'Vehicle {recording.vehicle_id} was recorded!'}


@router.get('/vehicles/', description='Get all vehicles')
async def get_all_vehicles(redis_client: RedisClient = Depends(get_redis_client)):
    try:
        vehicles = await redis_client.get_items()
        await redis_client.publish(channel=VEHICLE_CHANNELS, data=vehicles)
    except (PubSubError, ConnectionError, DataError) as error:
        logger.error(error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Service is unavailable!',
        )
    return {'message': 'Vehicles was got successfully'}

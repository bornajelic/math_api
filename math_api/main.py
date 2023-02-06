from fastapi import Depends, FastAPI, status

from math_api.utils.logger import CustomizeLogger
from math_api.utils.redis_db import redis_cache
from math_api.utils.schema import (
    AddData,
    DivideData,
    MultiplyData,
    ResponseModel,
    SubtractData,
)
from math_api.utils.settings import api_config

logger = CustomizeLogger.make_logger()
app = FastAPI(title="Math API", docs_url="/", debug=True)


@app.on_event("startup")
async def startup_event():
    redis_url = f"{api_config.HOST}:{api_config.PORT}/{api_config.DB}"
    await redis_cache.create_connection(redis_url=redis_url)


@app.get(
    "/add",
    include_in_schema=True,
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    name="math:add",
    description="Add two numbers",
)
async def add(input_data: AddData = Depends()):
    cached_res = True
    res = await redis_cache.get_item(input_data.key)
    if not res:
        res = input_data.x + input_data.y
        await redis_cache.setex_item(
            key=input_data.key, value=res, timedelta=api_config.TIMEDELTA
        )
        cached_res = False
    return ResponseModel(
        action="add", x=input_data.x, y=input_data.y, answer=res, cached=cached_res
    )


@app.get(
    "/subtract",
    include_in_schema=True,
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    name="math:subtract",
    description="Subtract two numbers",
)
async def subtract(input_data: SubtractData = Depends()):
    cached_res = True
    res = await redis_cache.get_item(input_data.key)
    if not res:
        res = input_data.x - input_data.y
        await redis_cache.setex_item(
            key=input_data.key, value=res, timedelta=api_config.TIMEDELTA
        )
        cached_res = False

    return ResponseModel(
        action="subtract", x=input_data.x, y=input_data.y, answer=res, cached=cached_res
    )


@app.get(
    "/multiply",
    include_in_schema=True,
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    name="math:multiply",
    description="Multiply two numbers",
)
async def multiply(input_data: MultiplyData = Depends()):
    cached_res = True
    res = await redis_cache.get_item(input_data.key)
    if not res:
        res = input_data.x * input_data.y
        await redis_cache.setex_item(
            key=input_data.key, value=res, timedelta=api_config.TIMEDELTA
        )
        cached_res = False

    return ResponseModel(
        action="multiply", x=input_data.x, y=input_data.y, answer=res, cached=cached_res
    )


@app.get(
    "/divide",
    include_in_schema=True,
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    name="math:divide",
    description="Divide two numbers",
)
async def divide(input_data: DivideData = Depends()):
    cached_res = True
    res = await redis_cache.get_item(input_data.key)
    if not res:
        res = input_data.x / input_data.y
        await redis_cache.setex_item(
            key=input_data.key, value=res, timedelta=api_config.TIMEDELTA
        )
        cached_res = False
    return ResponseModel(
        action="divide", x=input_data.x, y=input_data.y, answer=res, cached=cached_res
    )


@app.get(path="/health", name="health:default")
async def health():
    """Endpoint for checking the health of the application"""
    ping = await redis_cache.health()
    return {"API Health": "UP", "Redis Cache": ping}

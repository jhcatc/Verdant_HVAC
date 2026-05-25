import asyncio
import json
import redis.asyncio as redis
from app.core.ws_manager import manager

REDIS_URL = "redis://localhost:6379"

async def redis_listener():
    r = redis.from_url(REDIS_URL, decode_responses=True)
    pubsub = r.pubsub()

    await pubsub.subscribe("orders")

    async for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])

            # broadcast a todos los clientes WS
            await manager.broadcast(data)
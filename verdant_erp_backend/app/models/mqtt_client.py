import asyncio
import json
from asyncio_mqtt import Client
from app.core.database import async_session
from app.services.telemetry_service import ingest_telemetry

MQTT_BROKER = "localhost"
MQTT_TOPIC = "verdant/telemetry/#"


async def handle_message(message):
    payload = json.loads(message.payload.decode())

    async with async_session() as db:
        await ingest_telemetry(db, payload)


async def mqtt_worker():
    async with Client(MQTT_BROKER) as client:
        async with client.filtered_messages(MQTT_TOPIC) as messages:
            await client.subscribe(MQTT_TOPIC)

            async for msg in messages:
                await handle_message(msg)


def start_mqtt():
    loop = asyncio.get_event_loop()
    loop.create_task(mqtt_worker())
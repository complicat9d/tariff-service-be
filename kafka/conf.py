import orjson as json
from aiokafka import AIOKafkaProducer

from utils.time_utils import utcnow
from config import settings


class KafkaClient:
    def __init__(self, broker_url: str):
        self.broker_url = broker_url
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.broker_url, value_serializer=lambda v: json.dumps(v)
        )
        # Start the producer
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_log(
        self, action: str, user_id: int = None, cargo_type: str = None, date: str = None
    ):
        message = {
            "action": action,
            "timestamp": utcnow(),
        }
        if user_id:
            message.update({"user_id": user_id})
        if cargo_type:
            message.update({"cargo_type": cargo_type})
        if date:
            message.update({"date": date})
        await self.producer.send_and_wait("insurance_logs", message)


kafka_client = KafkaClient(broker_url=settings.KAFKA_BROKER)

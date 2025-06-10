from src.kafka.producer import KafkaProducer


class KafkaProducerService(KafkaProducer):
    KAFKA_TOPIC = "user_active"

    def __init__(self, topic: str = KAFKA_TOPIC):
        super().__init__()
        self.topic = topic

    async def send_data(self, user_data: dict):
        await self.send(self.topic, user_data)


user_kafka_producer = KafkaProducerService()

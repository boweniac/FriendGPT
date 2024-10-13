import redis


class RedisClient:
    def __init__(
            self,
            config: dict
    ):
        self.client = redis.Redis(
            host=config["host"],
            port=config["port"],
            db=0,
            decode_responses=True)
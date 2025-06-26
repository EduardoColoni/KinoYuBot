from models.redis.connection.redis_connection import RedisConnectionHandle
from models.redis.redis_repository import RedisRepository

redis_conn = RedisConnectionHandle().connect()
redis_repository = RedisRepository(redis_conn)

redis_repository.insert('estou', 'aquiii')

value = redis_repository.get('estou')

print(value)

redis_repository.delete('estou')
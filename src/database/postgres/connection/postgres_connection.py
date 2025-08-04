from .connection_options_postgres import connection_options_postgres
from psycopg2 import Error, pool

class PostgresPool:
    __pool = None

    @classmethod
    def init_pool(cls, minconn = 1, maxconn = 5):
        if cls.__pool is None:
            cls.__pool = pool.SimpleConnectionPool(
                minconn,
                maxconn,
                host=connection_options_postgres['HOST'],
                port=connection_options_postgres['PORT'],
                user=connection_options_postgres['USER'],
                password=connection_options_postgres['PASSWORD'],
                database=connection_options_postgres['DB_NAME']
            )

    @classmethod
    def get_conn(cls):
        if cls.__pool is None:
            raise RuntimeError("Connection pool not initialized")
        print("Conexão realizada ao banco")
        return cls.__pool.getconn()

    @classmethod
    def release_conn(cls, conn):
        if cls.__pool:
            cls.__pool.putconn(conn)
            print("Conexão retornada ao pool")

    @classmethod
    def close_all(cls):
        if cls.__pool:
            cls.__pool.closeall()
            print("Fechada todas conexões com o banco")


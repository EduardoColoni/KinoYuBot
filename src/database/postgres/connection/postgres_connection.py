from .connection_options_postgres import connection_options_postgres
import psycopg2 as pg
from psycopg2 import Error

class PostgresConnectionHandle:
    def __init__(self) -> None:
        """Inicializa o gerenciador de conexão com __conn=None"""
        self.__conn = None  # Atributo privado para armazenar a conexão

    def connect(self) -> pg.extensions.connection:
        """Estabelece conexão com o PostgreSQL usando as configurações importadas"""
        try:
            # Cria nova conexão usando os parâmetros do connection_options_postgres
            self.__conn = pg.connect(
                host=connection_options_postgres['HOST'],
                port=connection_options_postgres['PORT'],
                user=connection_options_postgres['USER'],
                password=connection_options_postgres['PASSWORD'],
                database=connection_options_postgres['DB_NAME']
            )
            print('Connected to PostgreSQL')
            return self.__conn
        except Error as e:
            # Log do erro e relança como RuntimeError para tratamento externo
            print(f"[ERRO BANCO] Falha ao conectar ao banco de dados: {e}")
            raise RuntimeError("Erro ao conectar ao banco de dados") from e

    def get_conn(self) -> pg.extensions.connection:
        """Retorna a conexão ativa (ou None se não conectado)"""
        return self.__conn

    def disconnect(self):
        """Fecha a conexão ativa se existir"""
        if self.__conn:
            self.__conn.close()
            print('PostgreSQL connection closed')
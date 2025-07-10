from src.database.postgres.connection.postgres_connection import PostgresConnectionHandle
import json

class PostgresRepository:
    def __init__(self) -> None:
        self.__db_handle = PostgresConnectionHandle()
        self.__conn = self.__db_handle.connect()
        self.__cursor = self.__conn.cursor()

    def insert_token(self, token_data: dict, streamer_id: str, guild_id: str, streamer_name: str) -> None:
        try:
            #Insere token em formato JSON no banco de dados
            self.__cursor.execute(
                "INSERT INTO streamer (token, streamer_id, guild_id, streamer_name) VALUES (%s, %s, %s, %s)",
                [json.dumps(token_data), streamer_id, guild_id, streamer_name]
            )
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to insert token: {e}")

    def select_token(self) -> any:
        try:
            self.__cursor.execute(
                "SELECT token FROM streamer ORDER BY id DESC LIMIT 1"
            )
            row = self.__cursor.fetchone()
            return row[0] if row else None  # Retorna o dicionário diretamente
        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to select token: {e}")

    def refresh_token(self, token_data: dict) -> None:
        try:
            #Insere token em formato JSON no banco de dados
            self.__cursor.execute(
                "UPDATE streamer SET token = %s WHERE id = (SELECT id FROM streamer ORDER BY id DESC LIMIT 1)",
                [json.dumps(token_data)]
            )
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to refresh token: {e}")

    def close(self) -> None:
        #Fecha cursor e conexão
        self.__cursor.close()
        self.__db_handle.disconnect()
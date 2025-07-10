from src.database.postgres.connection.postgres_connection import PostgresConnectionHandle
import json

class PostgresRepositoryRaffle:
    def __init__(self) -> None:
        self.__db_handle = PostgresConnectionHandle()
        self.__conn = self.__db_handle.connect()
        self.__cursor = self.__conn.cursor()

    def insert_itens(self, item: str, weigth: int, raffle_id: int, streamer_id: str) -> None:
        try:
            self.__cursor.execute(
                "INSERT INTO raffle_itens (item, weight, raffle_id, streamer_id) VALUES (%s, %s, %s, %s)",
                [str(item), int(weigth), int(raffle_id), str(streamer_id)],
            )
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to insert token: {e}")

    def select_token(self) -> any:
        try:
            self.__cursor.execute(
                "SELECT token FROM token_twitch ORDER BY id DESC LIMIT 1"
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
                "UPDATE token_twitch SET token = %s WHERE id = (SELECT id FROM token_twitch ORDER BY id DESC LIMIT 1)",
                [json.dumps(token_data)]
            )
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to refresh token: {e}")

    def select_guild_id(self, guild: str) -> any:
        try:
            self.__cursor.execute(
                "SELECT id FROM streamer WHERE guild_id = %s",
                [str(guild)]
            )
            return self.__cursor.fetchone()[0]
        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to find guild_id: {e}")

    def make_raffle_number(self, streamer_id:int):
        try:
            self.__cursor.execute(
                "SELECT COALESCE(MAX(raffle_id), 0) FROM raffle_itens WHERE streamer_id = %s;",
                [int(streamer_id)]
            )
            return self.__cursor.fetchone()[0]
        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed: {e}")


    def close(self) -> None:
        #Fecha cursor e conexão
        self.__cursor.close()
        self.__db_handle.disconnect()
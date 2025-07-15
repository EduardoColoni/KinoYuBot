from src.database.postgres.connection.postgres_connection import PostgresConnectionHandle

class PostgresRepositoryRaffle:
    def __init__(self) -> None:
        self.__db_handle = PostgresConnectionHandle()
        self.__conn = self.__db_handle.connect()
        self.__cursor = self.__conn.cursor()

    def insert_items(self, item: str, weight: int, raffle_id: int, guild_id: str) -> None:
        try:
            self.__cursor.execute(
                "SELECT insert_items(%s, %s, %s, %s)",
                [item, weight, raffle_id, guild_id]
            )
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to insert item: {e}")

    def make_raffle(self, guild_id: str):
        try:
            self.__cursor.execute(
                "SELECT make_raffle(%s)",
                [guild_id]
            )
            # fetchone() retornará uma tupla como (5, 10) se id=5 e raffle_id=10 forem sorteados
            result_tuple = self.__cursor.fetchone()
            if result_tuple:
                # result_tuple[0] será o id do item, result_tuple[1] será o raffle_id
                return result_tuple
            return None  # Retorna None se nenhum item for sorteado ou se a função retornar NULLs
        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to get raffle item IDs: {e}")

    def make_raffle_id(self, guild_id: str):
        try:
            self.__cursor.execute(
                """
                SELECT id FROM streamer 
                WHERE guild_id = %s;
                """,
                [guild_id]
            )
            streamer_id = self.__cursor.fetchone()
            if streamer_id is None:
                return None
            streamer_id = streamer_id[0]

        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to get streamer ID: {e}")

        try:
            self.__cursor.execute(
                """
                SELECT COALESCE(MAX(raffle_id), 0)
                FROM raffle_items
                WHERE streamer_id = %s;
                """,
                [streamer_id]
            )
            raffle_id = self.__cursor.fetchone()
            if raffle_id:
                return raffle_id[0] + 1
            return 1

        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to make raffle ID: {e}")

    def close(self) -> None:
        #Fecha cursor e conexão
        self.__cursor.close()
        self.__db_handle.disconnect()
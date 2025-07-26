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
                "SELECT * FROM make_raffle(%s);",
                [guild_id]
            )
            result = self.__cursor.fetchone()
            if result and all(result):
                selected_item_id, selected_raffle_round_id, streamer_platform_id = result
                return selected_item_id, selected_raffle_round_id, streamer_platform_id
            else:
                return None  # Nenhum item sorteado
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

    def update_item(self, winner_name: str, item_id: int, raffle_id: int):
        try:
            self.__cursor.execute(
                """
                    UPDATE raffle_items
                    SET winner = %s, 
                    update_at = NOW() 
                    WHERE id = %s AND raffle_id = %s;
                """,
                [winner_name, item_id, raffle_id]
            )
            self.__conn.commit()

        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to make raffle ID: {e}")

    def get_last_raffle_id(self, received_streamer_id: int):
        try:
            self.__cursor.execute(
                "SELECT MAX(raffle_id) FROM raffle_items WHERE streamer_id = %s;",
                [received_streamer_id]
            )
            raffle_id = self.__cursor.fetchone()[0]
            return int(raffle_id)
        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to get raffle id: {e}")

    def get_streamer_id(self, guild_id: str):
        try:
            self.__cursor.execute(
                "SELECT id FROM streamer WHERE guild_id = %s",
                [guild_id]
            )
            streamer_id = self.__cursor.fetchone()[0]
            return int(streamer_id)
        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to get raffle id: {e}")

    def verify_item_list(self, raffle_id: int):
        try:
            self.__cursor.execute(
                """
                SELECT item FROM raffle_items
                WHERE raffle_id = %s AND winner IS NULL;
                """,
                [raffle_id]
            )
            itens = self.__cursor.fetchall()
            return itens #Vai retornar uma lista dos itens com winner vazio, senão tiver nenhum vai retornar uma tupla vazia []
        except Exception as e:
            self.__conn.rollback()
            raise RuntimeError(f"Failed to verify item: {e}")

    def close(self) -> None:
        #Fecha cursor e conexão
        self.__cursor.close()
        self.__db_handle.disconnect()
import json

class PostgresRepositoryAuth:
    def __init__(self, conn):
        self.conn = conn  # Usa a conexão recebida

    def insert_token(self, token_data: dict, streamer_id: str, guild_id: str, streamer_name: str):
        try:
            #Insere token em formato JSON no banco de dados
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO streamer (token, streamer_id, guild_id, streamer_name) VALUES (%s, %s, %s, %s)", (json.dumps(token_data), streamer_id, guild_id, streamer_name))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Failed to insert token: {e}")

    def select_token(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT token FROM streamer ORDER BY id DESC LIMIT 1")
                row = cur.fetchone()
                return row[0] if row else None  # Retorna o dicionário diretamente
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Failed to select token: {e}")

    def refresh_token(self, token_data: dict) -> None:
        try:
            #Insere token em formato JSON no banco de dados
            with self.conn.cursor() as cur:
                cur.execute("UPDATE streamer SET token = %s WHERE id = (SELECT id FROM streamer ORDER BY id DESC LIMIT 1)", (json.dumps(token_data),))
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Failed to refresh token: {e}")
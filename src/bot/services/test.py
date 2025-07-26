from src.database.postgres.postgres_repository_raffle import PostgresRepositoryRaffle

def get_raffle_id(guild_id: str):
    repo_raffle = PostgresRepositoryRaffle()
    streamer_id = repo_raffle.get_streamer_id(guild_id)
    raffle_id = repo_raffle.get_last_raffle_id(streamer_id)
    return raffle_id

def can_run_func(user_input: bool, guild_id: str):
    repo_raffle = PostgresRepositoryRaffle()
    raffle_id = get_raffle_id(guild_id)
    item_list_active = repo_raffle.verify_item_list(raffle_id)
    raffle_status = True
    if not user_input or not item_list_active:
        raffle_status = False
    return raffle_status

def teste():
    user_input = input("Digite falso ou true")
    if user_input == "falso":
        user_input = False
    else:
        user_input = True

    resultado = can_run_func(user_input, "1387251515114389596")

    print(resultado)

teste()
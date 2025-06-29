from random import choices

def sorteio(itens = [], raffle = []):
    result = choices(itens, weights=raffle)
    return result
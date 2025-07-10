from random import choices

def sorteio(itens = [], peso = []):
    result = choices(itens, weights=peso)
    return result

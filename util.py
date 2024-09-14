import random

def generate_random_number(start=1, end=100):
    """
    Gera um número aleatório dentro do intervalo especificado.
    
    :param start: Valor inicial do intervalo (inclusivo)
    :param end: Valor final do intervalo (inclusivo)
    :return: Número inteiro aleatório
    """
    return random.randint(start, end)

def generate_random_prime(start=2, end=100):
    """
    Gera um número primo aleatório dentro do intervalo especificado.
    
    :param start: Valor inicial do intervalo (inclusivo)
    :param end: Valor final do intervalo (inclusivo)
    :return: Número primo aleatório
    """
    is_prime = lambda n: n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))
    while True:
        num = generate_random_number(start, end)
        if is_prime(num):
            return num

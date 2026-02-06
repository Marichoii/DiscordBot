import random
from typing import Dict, List, TypeVar

T = TypeVar('T')

instinto_comida: List[str] = [
    "comida?",
    "fome.",
    "definhando",
    "isso era meu",
    "cadê o rango",
    "preciso mastigar algo"
]
instinto_passeio: List[str] = [
    "rua?",
    "guia.",
    "agora.",
    "latindo pro nada",
    "cheirinhos novos",
    "porta. agora."
]
instinto_gato: List[str] = [
    "inimigo.",
    "grrr",
    "não gosto disso",
    "onde",
    "olhos felinos detectados",
    "não me provoca"
]
instinto_bola: List[str] = [
    "minha.",
    "joga.",
    "não tira.",
    "só joga",
    "cê viu? bola!",
    "prioridade: bola"
]

nao_sei: List[str] = [
    "não entendi",
    "cérebro liso",
    "latindo confusa",
    "isso não é da minha espécie",
    "meu processador é de cachorro",
    "dormi no meio da frase"
]

brainrot: List[str] = [
    "???",
    "mds",
    "não",
    "para",
    "socorro",
    "não sei ler",
    "au?",
    "travei",
    "erro 404: cérebro"
]

respostas_erradas: List[str] = [
    "sim (errado)",
    "não (talvez)",
    "com certeza não",
    "acho que sim mas não",
    "entendi tudo errado",
    "tenho certeza de nada"
]

emojis: List[str] = ["🐶", "🦴", "💤", "😵‍💫", "🤨", "🧠", "❔", "🐾"]
latidos: List[str] = ["au", "au au", "grr", "woof", "wuf", "auuu"]

lembrancas: List[str] = [
    "acho que vc falou {word}",
    "vc vive dizendo {word}",
    "isso me lembra {word}",
    "já ouvi {word} antes",
    "não era vc que falou {word}?",
    "guardei {word} no meu focinho"
]

lembrancas_erradas: List[str] = [
    "vc sempre fala pizza (mentira)",
    "acho que vc disse abacate",
    "vc falou algo tipo blablabla",
    "era alguma coisa com s né",
    "acho que foi 'pipoca'",
    "talvez fosse 'banana'?"
]

_last_pick: Dict[str, str] = {}

def pick(lista: List[T]) -> T:
    """Escolhe um item aleatório da lista."""
    return random.choice(lista)


def pick_unique(key: str, lista: List[str]) -> str:
    """Evita repetir a última resposta para o mesmo key."""
    if not lista:
        return ""
    if len(lista) == 1:
        return lista[0]
    last = _last_pick.get(key)
    choice = random.choice(lista)
    while choice == last:
        choice = random.choice(lista)
    _last_pick[key] = choice
    return choice

import random
from typing import List, TypeVar

T = TypeVar('T')

instinto_comida: List[str] = ["comida?", "fome.", "definhando", "isso era meu"]
instinto_passeio: List[str] = ["rua?", "guia.", "agora.", "latindo pro nada"]
instinto_gato: List[str] = ["inimigo.", "grrr", "não gosto disso", "onde"]
instinto_bola: List[str] = ["minha.", "joga.", "não tira.", "só joga"]

nao_sei: List[str] = [
    "não entendi",
    "cérebro liso",
    "latindo confusa",
    "isso não é da minha espécie"
]

brainrot: List[str] = [
    "???",
    "mds",
    "não",
    "para",
    "socorro",
    "não sei ler",
    "au?"
]

respostas_erradas: List[str] = [
    "sim (errado)",
    "não (talvez)",
    "com certeza não",
    "acho que sim mas não",
    "entendi tudo errado"
]

emojis: List[str] = ["🐕", "🦴", "💤", "😵‍💫", "🤨", "🧠", "❓"]
latidos: List[str] = ["au", "au au", "grr", "woof"]

lembrancas: List[str] = [
    "acho que vc falou {word}",
    "vc vive dizendo {word}",
    "isso me lembra {word}",
    "já ouvi {word} antes",
    "não era vc que falou {word}?"
]

lembrancas_erradas: List[str] = [
    "vc sempre fala pizza (mentira)",
    "acho que vc disse abacate",
    "vc falou algo tipo blablabla",
    "era alguma coisa com s né"
]

def pick(lista: List[T]) -> T:
    """Escolhe um item aleatório da lista."""
    return random.choice(lista)

import random
from typing import Optional

learned_words: set[str] = set()

def learn(word: str) -> None:
    """Aprende uma nova palavra se tiver 4 ou mais caracteres."""
    if len(word) >= 4:
        learned_words.add(word)

def random_learned() -> Optional[str]:
    """Retorna uma palavra aleatória do vocabulário aprendido."""
    if learned_words:
        return random.choice(list(learned_words))
    return None

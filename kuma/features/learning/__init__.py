import random
from typing import Optional

learned_words: set[str] = set()

def learn(word: str) -> None:
    """Aprende uma nova palavra se tiver 4+ caracteres e for alfanumérica."""
    cleaned = word.strip().lower()
    if len(cleaned) >= 4 and cleaned.isalnum():
        learned_words.add(cleaned)

def random_learned() -> Optional[str]:
    """Retorna uma palavra aleatória do vocabulário aprendido."""
    if learned_words:
        return random.choice(list(learned_words))
    return None

from typing import List

def contains(msg: str, palavras: List[str]) -> bool:
    """Verifica se a mensagem contém alguma das palavras da lista."""
    return any(p in msg for p in palavras)

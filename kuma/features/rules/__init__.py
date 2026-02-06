from typing import List
import re


def contains(msg: str, palavras: List[str]) -> bool:
    """Verifica se a mensagem contém alguma das palavras da lista."""
    for p in palavras:
        if re.search(rf"\b{re.escape(p)}\b", msg):
            return True
    return False

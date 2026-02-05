from typing import List

FEARS: List[str] = ["aspirador", "fogos", "banho", "veterinário"]

def scared_by(msg: str) -> bool:
    """Verifica se a mensagem contém algo que assusta a Kuma."""
    return any(fear in msg for fear in FEARS)

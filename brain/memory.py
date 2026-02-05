import time
from typing import Optional

user_memory: dict[int, str] = {}
last_used: dict[int, float] = {}

COOLDOWN = 60  # segundos

def remember(user: int, msg: str) -> None:
    """Lembra a última palavra dita por um usuário."""
    words = msg.split()
    if words:
        user_memory[user] = words[-1]

def can_recall(user: int) -> bool:
    """Verifica se pode usar lembrança (cooldown)."""
    now = time.time()
    last = last_used.get(user, 0)
    if now - last > COOLDOWN:
        last_used[user] = now
        return True
    return False

def recall_user(user: int) -> Optional[str]:
    """Recupera a última palavra lembrada de um usuário."""
    return user_memory.get(user)

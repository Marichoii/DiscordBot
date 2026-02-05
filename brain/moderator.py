import time

_mod_until: float = 0

def activate_mod(seconds: int = 10) -> None:
    """Ativa o modo moderador por X segundos."""
    global _mod_until
    _mod_until = time.time() + seconds

def is_mod() -> bool:
    """Verifica se o modo moderador está ativo."""
    return time.time() < _mod_until

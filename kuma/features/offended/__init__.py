import time

_offended_until: float = 0

def offend(seconds: int = 30) -> None:
    """Define que a Kuma está ofendida por X segundos."""
    global _offended_until
    _offended_until = time.time() + seconds

def is_offended() -> bool:
    """Verifica se a Kuma está ofendida."""
    return time.time() < _offended_until

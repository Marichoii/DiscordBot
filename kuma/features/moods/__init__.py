from datetime import datetime
import random
from typing import Literal

MoodType = Literal["cansada", "hiper", "normal"]

def time_based_mood() -> MoodType:
    """Determina o humor da Kuma baseado na hora do dia."""
    hour = datetime.now().hour
    if 0 <= hour <= 6:
        return "cansada"
    if 7 <= hour <= 12:
        return random.choice(["normal", "hiper"])
    if 13 <= hour <= 18:
        return "normal"
    return random.choice(["hiper", "cansada"])

def mood_modifier(mood: MoodType, text: str) -> str:
    """Modifica o texto baseado no humor atual."""
    if mood == "cansada":
        return text + "..."
    if mood == "hiper":
        return text + "!!!"
    return text

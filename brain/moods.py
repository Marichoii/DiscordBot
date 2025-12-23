from datetime import datetime
import random

def time_based_mood():
    hour = datetime.now().hour
    if 0 <= hour <= 6:
        return "cansada"
    if 7 <= hour <= 12:
        return random.choice(["normal", "hiper"])
    if 13 <= hour <= 18:
        return "normal"
    return random.choice(["hiper", "cansada"])

def mood_modifier(mood, text):
    if mood == "cansada":
        return text + "..."
    if mood == "hiper":
        return text + "!!!"
    return text

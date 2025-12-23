learned_words = set()

def learn(word):
    if len(word) >= 4:
        learned_words.add(word)

def random_learned():
    if learned_words:
        return list(learned_words)[-1]
    return None

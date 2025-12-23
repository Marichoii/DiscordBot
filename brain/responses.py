import random

instinto_comida = ["comida?", "fome.", "definhando", "isso era meu"]
instinto_passeio = ["rua?", "guia.", "agora.", "latindo pro nada"]
instinto_gato = ["inimigo.", "grrr", "não gosto disso", "onde"]
instinto_bola = ["minha.", "joga.", "não tira.", "só joga"]

nao_sei = [
    "não entendi",
    "cérebro liso",
    "latindo confusa",
    "isso não é da minha espécie"
]

brainrot = [
    "???",
    "mds",
    "não",
    "para",
    "socorro",
    "não sei ler",
    "au?"
]

respostas_erradas = [
    "sim (errado)",
    "não (talvez)",
    "com certeza não",
    "acho que sim mas não",
    "entendi tudo errado"
]

emojis = ["🐕", "🦴", "💤", "😵‍💫", "🤨", "🧠", "❓"]
latidos = ["au", "au au", "grr", "woof"]

lembrancas = [
    "acho que vc falou {word}",
    "vc vive dizendo {word}",
    "isso me lembra {word}",
    "já ouvi {word} antes",
    "não era vc que falou {word}?"
]

lembrancas_erradas = [
    "vc sempre fala pizza (mentira)",
    "acho que vc disse abacate",
    "vc falou algo tipo blablabla",
    "era alguma coisa com s né"
]

def pick(lista):
    return random.choice(lista)

import discord
import os
import random
import asyncio
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from brain.memory import can_recall
from brain.responses import lembrancas, lembrancas_erradas

from brain.moods import time_based_mood, mood_modifier
from brain.learning import learn, random_learned, learned_words
from brain.fear import scared_by, FEARS
from brain.moderator import activate_mod, is_mod
from brain.memory import remember, recall_user
from brain.rules import contains
from brain.offended import offend, is_offended
from brain.responses import (
    instinto_comida,
    instinto_passeio,
    instinto_gato,
    instinto_bola,
    nao_sei,
    brainrot,
    respostas_erradas,
    emojis,
    latidos,
    pick
)

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"🐕 kuma online: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()
    for w in msg.split():
        learn(w)

    remember(message.author.id, msg)
    mood = time_based_mood()

    # Sistema de medo
    if scared_by(msg):
        await message.channel.send("NÃO. MEDO. SOCORRO.")
        return

    # Ativa modo moderador
    if "kuma mod" in msg:
        activate_mod(10)
        await message.channel.send("sou mod agora 😤")
        return

    # Moderação ativa
    if is_mod() and contains(msg, ["idiota", "burro", "xingar"]):
        await message.delete()
        await message.channel.send("apaguei 👍")
        return

    # Sistema de ofensa
    if is_offended():
        await message.channel.send("não fala comigo 😤")
        return

    # Reação a bots
    if message.author.bot and random.random() < 0.3:
        await message.channel.send("vc é estranho")
        return

    # Surto de latidos aleatório
    if random.random() < 0.01:
        for _ in range(random.randint(3, 6)):
            await message.channel.send(pick(latidos))
            await asyncio.sleep(0.5)
        return

    # Brainrot aleatório
    if random.random() < 0.02:
        await message.channel.send(pick(brainrot))
        return

    # Instintos caninos
    if contains(msg, ["comida", "petisco", "fome", "comer"]):
        await message.channel.send(mood_modifier(mood, pick(instinto_comida)))
        return

    if contains(msg, ["passear", "rua", "passeio"]):
        await message.channel.send(mood_modifier(mood, pick(instinto_passeio)))
        return

    if contains(msg, ["gato"]):
        await message.channel.send(mood_modifier(mood, pick(instinto_gato)))
        return

    if contains(msg, ["bola", "brinquedo"]):
        await message.channel.send(mood_modifier(mood, pick(instinto_bola)))
        return

    # Quando mencionam a kuma
    if "kuma" in msg or bot.user.mentioned_in(message):
        if contains(msg, ["chata", "burra", "feia"]):
            offend(45)
            await message.channel.send("fiquei triste 😢")
            return

        if random.random() < 0.2:
            await message.channel.send(pick(respostas_erradas))
            return

        if random.random() < 0.3:
            await message.channel.send(pick(emojis))
            return

        lembranca = recall_user(message.author.id)
        if lembranca and can_recall(message.author.id):
            if random.random() < 0.3:
                await message.channel.send(pick(lembrancas_erradas))
                return

            frase = pick(lembrancas).format(word=lembranca)
            await message.channel.send(frase)
            return

        learned = random_learned()
        if learned and random.random() < 0.1:
            await message.channel.send(f"aprendi a palavra {learned}")
            return

        await message.channel.send(pick(nao_sei))

    await bot.process_commands(message)

# ============= COMANDOS SLASH =============

@bot.tree.command(name="kuma", description="invoca a kuma")
async def kuma_slash(interaction: discord.Interaction):
    mood = time_based_mood()
    resposta = mood_modifier(mood, pick(brainrot + nao_sei))
    await interaction.response.send_message(resposta)

@bot.tree.command(name="humor", description="vê o humor atual da kuma")
async def humor(interaction: discord.Interaction):
    mood = time_based_mood()
    emocoes = {
        "cansada": "tô com sono... 😴💤",
        "hiper": "HIPERATIVA!!! ENERGIA!!! 🐕⚡",
        "normal": "tô de boa 🐶"
    }
    await interaction.response.send_message(emocoes.get(mood, "confusa"))

@bot.tree.command(name="petisco", description="dá um petisco pra kuma")
async def petisco(interaction: discord.Interaction):
    respostas = [
        "COMIDA!!! *come desesperada*",
        "gostoso 🦴",
        "mais.",
        "isso era tudo?",
        "onde tem mais?",
        "*engoliu sem mastigar*"
    ]
    await interaction.response.send_message(pick(respostas))

@bot.tree.command(name="carinho", description="faz carinho na kuma")
async def carinho(interaction: discord.Interaction):
    if is_offended():
        await interaction.response.send_message("não quero 😤")
        return
    
    respostas = [
        "*balança o rabo*",
        "de novo",
        "*deita de barriga pra cima*",
        "🐕💕",
        "não para",
        "*vira a cabeça pro lado e fica feliz*"
    ]
    await interaction.response.send_message(pick(respostas))

@bot.tree.command(name="passear", description="convida a kuma pra passear")
async def passear(interaction: discord.Interaction):
    respostas = [
        "RUA??? RUA??? *pula desesperada*",
        "AGORAAA",
        "*já tá na porta*",
        "pega a guia rápido",
        "VAMO VAMO VAMO",
        "*rodando em círculos*"
    ]
    await interaction.response.send_message(pick(respostas))

@bot.tree.command(name="truque", description="pede pra kuma fazer um truque")
async def truque(interaction: discord.Interaction):
    truques = [
        "senta! (mas não sentou)",
        "*late pra parede*",
        "*deita no lugar errado*",
        "finge que sabe dar a pata",
        "*rola no chão aleatoriamente*",
        "fica olhando confusa",
        "au? isso era um truque?"
    ]
    await interaction.response.send_message(pick(truques))

@bot.tree.command(name="medos", description="lista os medos da kuma")
async def medos(interaction: discord.Interaction):
    lista_medos = ", ".join(FEARS)
    await interaction.response.send_message(f"tenho medo de: {lista_medos} 😰")

@bot.tree.command(name="vocabulario", description="mostra quantas palavras a kuma aprendeu")
async def vocabulario(interaction: discord.Interaction):
    total = len(learned_words)
    if total == 0:
        await interaction.response.send_message("ainda não aprendi nada 🧠❌")
    elif total < 10:
        await interaction.response.send_message(f"sei {total} palavras (quase nada)")
    elif total < 50:
        await interaction.response.send_message(f"sei {total} palavras! tô ficando esperta 🧠")
    else:
        await interaction.response.send_message(f"sei {total} palavras!! sou um gênio canino 🧠✨")

@bot.tree.command(name="latir", description="faz a kuma latir")
async def latir(interaction: discord.Interaction):
    await interaction.response.send_message("au au!")
    await asyncio.sleep(0.5)
    for _ in range(random.randint(2, 4)):
        await interaction.channel.send(pick(latidos))
        await asyncio.sleep(0.4)

@bot.tree.command(name="status", description="status completo da kuma")
async def status(interaction: discord.Interaction):
    mood = time_based_mood()
    vocab = len(learned_words)
    
    embed = discord.Embed(
        title="🐕 Status da Kuma",
        color=discord.Color.orange()
    )
    embed.add_field(name="Humor", value=mood, inline=True)
    embed.add_field(name="Vocabulário", value=f"{vocab} palavras", inline=True)
    embed.add_field(name="Estado", value="ofendida 😤" if is_offended() else "de boa", inline=True)
    embed.add_field(name="Poder", value="mod ativa 😎" if is_mod() else "cachorra comum", inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="desculpa", description="pede desculpas pra kuma")
async def desculpa(interaction: discord.Interaction):
    if not is_offended():
        await interaction.response.send_message("nem tava brava 🐶")
    else:
        offend(0)  # Remove a ofensa
        await interaction.response.send_message("tá bom né... *perdoou mas tá de cara ainda*")

@bot.tree.command(name="ajuda", description="lista dos comandos da kuma")
async def ajuda(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📋 Comandos da Kuma",
        description="sou uma spitz caótica, esses são meus comandos:",
        color=discord.Color.gold()
    )
    
    comandos = [
        ("/kuma", "invoca a kuma"),
        ("/humor", "vê meu humor atual"),
        ("/petisco", "me dá comida"),
        ("/carinho", "faz carinho"),
        ("/passear", "me convida pra passear"),
        ("/truque", "peço pra fazer truque"),
        ("/medos", "lista meus medos"),
        ("/vocabulario", "quantas palavras sei"),
        ("/latir", "me faz latir"),
        ("/status", "meu status completo"),
        ("/desculpa", "pede desculpas"),
        ("/ajuda", "essa mensagem")
    ]
    
    for cmd, desc in comandos:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    embed.set_footer(text="também respondo quando falam 'kuma' nas mensagens!")
    
    await interaction.response.send_message(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
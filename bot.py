import discord
import os
import random
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from brain.memory import can_recall
from brain.responses import lembrancas, lembrancas_erradas

from brain.moods import time_based_mood, mood_modifier
from brain.learning import learn, random_learned
from brain.fear import scared_by
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
    lembrancas,
    lembrancas_erradas,
    pick
)

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"kuma online: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()
    for w in msg.split():
        learn(w)

    remember(message.author.id, msg)
    mood = time_based_mood()

    if scared_by(msg):
        await message.channel.send("NÃO. MEDO. SOCORRO.")
        return

    if "kuma mod" in msg:
        activate_mod(10)
        await message.channel.send("sou mod agora")
        return

    if is_mod() and contains(msg, ["idiota", "burro", "xingar"]):
        await message.delete()
        await message.channel.send("apaguei 👍")
        return

    if is_offended():
        await message.channel.send("não fala comigo")
        return

    if message.author.bot and random.random() < 0.3:
        await message.channel.send("vc é estranho")
        return

    if random.random() < 0.01:
        for _ in range(random.randint(3, 6)):
            await message.channel.send(pick(latidos))
            await asyncio.sleep(0.5)
        return

    if random.random() < 0.02:
        await message.channel.send(pick(brainrot))
        return

    if contains(msg, ["comida", "petisco", "fome"]):
        await message.channel.send(mood_modifier(mood, pick(instinto_comida)))
        return

    if contains(msg, ["passear", "rua"]):
        await message.channel.send(mood_modifier(mood, pick(instinto_passeio)))
        return

    if contains(msg, ["gato"]):
        await message.channel.send(mood_modifier(mood, pick(instinto_gato)))
        return

    if contains(msg, ["bola", "brinquedo"]):
        await message.channel.send(mood_modifier(mood, pick(instinto_bola)))
        return

    if "kuma" in msg or bot.user.mentioned_in(message):

        if contains(msg, ["chata", "burra", "feia"]):
            offend(45)
            await message.channel.send("fiquei triste")
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

@bot.tree.command(name="kuma", description="invoca a kuma")
async def kuma_slash(interaction: discord.Interaction):
    mood = time_based_mood()
    resposta = mood_modifier(mood, pick(brainrot + nao_sei))
    await interaction.response.send_message(resposta)

bot.run(os.getenv("DISCORD_TOKEN"))

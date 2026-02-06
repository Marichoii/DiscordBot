# -*- coding: utf-8 -*-
import asyncio
import logging
import os
import random
from typing import cast

import discord
from discord.abc import Messageable
from discord.ext import commands, tasks
from dotenv import load_dotenv

from kuma.app.config import CONFIG
from kuma.app.ratelimit import Cooldown
from kuma.app.text import normalize, tokenize
from kuma.features.fear import FEARS, scared_by
from kuma.features.learning import learn, learned_words, random_learned
from kuma.features.memory import can_recall, recall_user, remember
from kuma.features.moderator import activate_mod, is_mod
from kuma.features.moods import mood_modifier, time_based_mood
from kuma.features.offended import offend, is_offended
from kuma.features.persistence import export_state, import_state, load_data, save_data
from kuma.features.responses import (
    brainrot,
    emojis,
    instinto_bola,
    instinto_comida,
    instinto_gato,
    instinto_passeio,
    latidos,
    lembrancas,
    lembrancas_erradas,
    nao_sei,
    pick,
    pick_unique,
    respostas_erradas,
)
from kuma.features.rules import contains

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("kuma.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=CONFIG.prefix, intents=intents)

user_cooldown = Cooldown(CONFIG.on_message_user_cooldown)
channel_cooldown = Cooldown(CONFIG.on_message_channel_cooldown)
slash_cooldown = Cooldown(CONFIG.slash_user_cooldown)

async def send_channel(channel: Messageable, *args, **kwargs):
    """Envia mensagem garantindo canal messageable para o type checker."""
    return await channel.send(*args, **kwargs)
EMBED_COLOR = discord.Color.from_rgb(255, 199, 145)


def style_embed(embed: discord.Embed, interaction: discord.Interaction) -> discord.Embed:
    user = interaction.client.user
    embed.color = EMBED_COLOR
    if user:
        embed.set_author(
            name=f"{user.name} • Kuma",
            icon_url=user.display_avatar.url,
        )
    embed.set_footer(text="🐾 Kuma • Skinwalker")
    embed.timestamp = discord.utils.utcnow()
    return embed


async def safe_send(interaction: discord.Interaction, *args, **kwargs):
    """Envia resposta lidando com interações já reconhecidas/expiradas."""
    try:
        if interaction.response.is_done():
            return await interaction.followup.send(*args, **kwargs)
        return await interaction.response.send_message(*args, **kwargs)
    except discord.errors.NotFound:
        # Interação expirada; não há mais o que fazer
        return None
    except discord.errors.HTTPException as e:
        # 40060 = Interaction has already been acknowledged
        if getattr(e, "code", None) == 40060:
            return None
        raise


async def guard_slash(interaction: discord.Interaction) -> bool:
    if slash_cooldown.ready(interaction.user.id):
        return True
    await safe_send(interaction, "calma aí... tenta de novo em instantes", ephemeral=True)
    return False


@bot.event
async def on_ready():
    """Evento chamado quando o bot está pronto."""
    try:
        data = load_data()
        import_state(data)

        await bot.tree.sync()
        logger.info(f"🐶 kuma online: {bot.user}")
        print(f"🐶 kuma online: {bot.user}")

        if not auto_save.is_running():
            auto_save.start()
            logger.info("Sistema de salvamento automático iniciado")
    except Exception as e:
        logger.error(f"Erro no on_ready: {e}", exc_info=True)


@tasks.loop(minutes=CONFIG.autosave_minutes)
async def auto_save():
    """Salva dados automaticamente a cada X minutos."""
    try:
        data = export_state()
        save_data(data)
    except Exception as e:
        logger.error(f"Erro no salvamento automático: {e}", exc_info=True)


@bot.event
async def on_message(message: discord.Message):
    """Evento chamado quando uma mensagem é recebida."""
    if message.author == bot.user:
        return

    try:
        msg = normalize(message.content)
        words = tokenize(msg)

        for w in words:
            learn(w)

        remember(message.author.id, msg)

        if not user_cooldown.ready(message.author.id) or not channel_cooldown.ready(
            message.channel.id
        ):
            await bot.process_commands(message)
            return

        mood = time_based_mood()

        # Sistema de medo
        if scared_by(msg):
            await send_channel(cast(Messageable, message.channel), CONFIG.fear_reply)
            return

        # Ativa modo moderador
        if "kuma mod" in msg:
            if message.guild and isinstance(message.author, discord.Member) and message.author.guild_permissions.manage_messages:
                activate_mod(CONFIG.mod_duration_seconds)
                await send_channel(cast(Messageable, message.channel), "sou mod agora 😤")
            else:
                await send_channel(cast(Messageable, message.channel), "sem permissão pra isso 🙅")
            return

        # Moderação ativa
        if is_mod() and contains(msg, ["idiota", "burro", "xingar"]):
            try:
                await message.delete()
                await send_channel(cast(Messageable, message.channel), "apaguei 👍")
            except discord.Forbidden:
                await send_channel(cast(Messageable, message.channel), "não tenho permissão pra apagar 😔")
            except Exception as e:
                logger.error(f"Erro ao deletar mensagem: {e}")
            return

        # Sistema de ofensa
        if is_offended():
            await send_channel(cast(Messageable, message.channel), "não fala comigo 😤")
            return

        # Reação a bots
        if message.author.bot and random.random() < CONFIG.respond_to_bots_chance:
            await send_channel(cast(Messageable, message.channel), "vc é estranho")
            return

        # Surto de latidos aleatório
        if random.random() < CONFIG.bark_burst_chance:
            for _ in range(random.randint(3, 6)):
                await send_channel(cast(Messageable, message.channel), pick(latidos))
                await asyncio.sleep(0.5)
            return

        # Brainrot aleatório
        if random.random() < CONFIG.brainrot_chance:
            await send_channel(cast(Messageable, message.channel), pick(brainrot))
            return

        # Instintos caninos
        if contains(msg, ["comida", "petisco", "fome", "comer"]):
            await send_channel(cast(Messageable, message.channel), 
                mood_modifier(mood, pick_unique(f"comida:{message.channel.id}", instinto_comida))
            )
            return

        if contains(msg, ["passear", "rua", "passeio"]):
            await send_channel(cast(Messageable, message.channel), 
                mood_modifier(mood, pick_unique(f"passeio:{message.channel.id}", instinto_passeio))
            )
            return

        if contains(msg, ["gato"]):
            await send_channel(cast(Messageable, message.channel), 
                mood_modifier(mood, pick_unique(f"gato:{message.channel.id}", instinto_gato))
            )
            return

        if contains(msg, ["bola", "brinquedo"]):
            await send_channel(cast(Messageable, message.channel), 
                mood_modifier(mood, pick_unique(f"bola:{message.channel.id}", instinto_bola))
            )
            return

        # Quando mencionam a kuma
        if "kuma" in msg or (bot.user and bot.user.mentioned_in(message)):
            # Intenções simples
            if contains(msg, ["late", "latir", "lata", "latindo"]):
                await send_channel(cast(Messageable, message.channel), "au au!")
                for _ in range(random.randint(1, 3)):
                    await asyncio.sleep(0.4)
                    await send_channel(cast(Messageable, message.channel), pick(latidos))
                return

            if contains(msg, ["petisco", "comida", "ração", "racao"]):
                await send_channel(
                    cast(Messageable, message.channel),
                    pick_unique(
                        f"petisco:{message.channel.id}",
                        [
                            "AAAAA PETISCO!!!",
                            "aceito. agora.",
                            "*come sem mastigar*",
                            "isso aí é respeito",
                            "obrigada. mais?",
                        ],
                    ),
                )
                return

            if contains(msg, ["passeia", "passear", "passeio", "rua"]):
                await send_channel(
                    cast(Messageable, message.channel),
                    pick_unique(f"passeio_call:{message.channel.id}", instinto_passeio),
                )
                return

            if contains(msg, ["carinho", "cafune", "afago"]):
                if is_offended():
                    await send_channel(cast(Messageable, message.channel), "não quero 😤")
                    return
                await send_channel(
                    cast(Messageable, message.channel),
                    pick_unique(
                        f"carinho_call:{message.channel.id}",
                        [
                            "*balança o rabo*",
                            "de novo",
                            "*deita de barriga pra cima*",
                            "gostei. continua.",
                            "isso é vida boa",
                        ],
                    ),
                )
                return

            if contains(msg, ["truque", "faz algo", "faz um truque"]):
                await send_channel(
                    cast(Messageable, message.channel),
                    pick_unique(
                        f"truque_call:{message.channel.id}",
                        [
                            "senta! (mas não sentou)",
                            "*rola no chão aleatoriamente*",
                            "finge que sabe dar a pata",
                            "*late pra parede*",
                            "au? isso era um truque?",
                        ],
                    ),
                )
                return

            if contains(msg, ["status", "como você tá", "como voce ta", "como vc ta"]):
                mood = time_based_mood()
                vocab = len(learned_words)
                await send_channel(
                    cast(Messageable, message.channel),
                    f"humor: {mood} | palavras: {vocab} | estado: {'ofendida' if is_offended() else 'de boa'}",
                )
                return

            if contains(msg, ["chata", "burra", "feia"]):
                offend(CONFIG.offended_duration_seconds)
                await send_channel(cast(Messageable, message.channel), "fiquei triste 😢")
                return

            if random.random() < CONFIG.kuma_mention_wrong_chance:
                await send_channel(cast(Messageable, message.channel), 
                    pick_unique(f"erradas:{message.channel.id}", respostas_erradas)
                )
                return

            if random.random() < CONFIG.kuma_mention_emoji_chance:
                await send_channel(cast(Messageable, message.channel), pick_unique(f"emoji:{message.channel.id}", emojis))
                return

            lembranca = recall_user(message.author.id)
            if lembranca and can_recall(message.author.id):
                if random.random() < CONFIG.kuma_recall_wrong_chance:
                    await send_channel(cast(Messageable, message.channel), 
                        pick_unique(f"lembranca_errada:{message.channel.id}", lembrancas_erradas)
                    )
                    return

                frase = pick_unique(f"lembranca:{message.channel.id}", lembrancas).format(
                    word=lembranca
                )
                await send_channel(cast(Messageable, message.channel), frase)
                return

            learned = random_learned()
            if learned and random.random() < CONFIG.kuma_learned_chance:
                await send_channel(cast(Messageable, message.channel), f"aprendi a palavra {learned}")
                return

            await send_channel(cast(Messageable, message.channel), pick_unique(f"nao_sei:{message.channel.id}", nao_sei))

        await bot.process_commands(message)

    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)


# ============= COMANDOS SLASH =============

@bot.tree.command(name="kuma", description="invoca a kuma")
async def kuma_slash(interaction: discord.Interaction):
    """Invoca a Kuma."""
    try:
        if not await guard_slash(interaction):
            return
        mood = time_based_mood()
        resposta = mood_modifier(mood, pick_unique("slash:kuma", brainrot + nao_sei))
        await safe_send(interaction, resposta)
    except Exception as e:
        logger.error(f"Erro no comando /kuma: {e}", exc_info=True)
        await safe_send(interaction, "erro... cérebro travou 🧠❌", ephemeral=True)


@bot.tree.command(name="humor", description="vê o humor atual da kuma")
async def humor(interaction: discord.Interaction):
    """Mostra o humor atual da Kuma."""
    try:
        if not await guard_slash(interaction):
            return
        mood = time_based_mood()
        emocoes = {
            "cansada": "tô com sono... 😴💤",
            "hiper": "HIPERATIVA!!! ENERGIA!!! 🐶⚡",
            "normal": "tô de boa 🐶",
        }
        await safe_send(interaction, emocoes.get(mood, "confusa"))
    except Exception as e:
        logger.error(f"Erro no comando /humor: {e}", exc_info=True)
        await safe_send(interaction, "não sei como tô me sentindo 😵‍💫", ephemeral=True)


@bot.tree.command(name="petisco", description="dá um petisco pra kuma")
async def petisco(interaction: discord.Interaction):
    """Dá um petisco para a Kuma."""
    try:
        if not await guard_slash(interaction):
            return
        respostas = [
            "COMIDA!!! *come desesperada*",
            "gostoso 🦴",
            "mais.",
            "isso era tudo?",
            "onde tem mais?",
            "*engoliu sem mastigar*",
        ]
        await safe_send(interaction, pick_unique("slash:petisco", respostas))
    except Exception as e:
        logger.error(f"Erro no comando /petisco: {e}", exc_info=True)
        await safe_send(interaction, "engasguei 😵", ephemeral=True)


@bot.tree.command(name="carinho", description="faz carinho na kuma")
async def carinho(interaction: discord.Interaction):
    """Faz carinho na Kuma."""
    try:
        if not await guard_slash(interaction):
            return
        if is_offended():
            await safe_send(interaction, "não quero 😤")
            return

        respostas = [
            "*balança o rabo*",
            "de novo",
            "*deita de barriga pra cima*",
            "🐶💞",
            "não para",
            "*vira a cabeça pro lado e fica feliz*",
        ]
        await safe_send(interaction, pick_unique("slash:carinho", respostas))
    except Exception as e:
        logger.error(f"Erro no comando /carinho: {e}", exc_info=True)
        await safe_send(interaction, "confusa 🤨", ephemeral=True)


@bot.tree.command(name="passear", description="convida a kuma pra passear")
async def passear(interaction: discord.Interaction):
    """Convida a Kuma para passear."""
    try:
        if not await guard_slash(interaction):
            return
        respostas = [
            "RUA??? RUA??? *pula desesperada*",
            "AGORAAA",
            "*já tá na porta*",
            "pega a guia rápido",
            "VAMO VAMO VAMO",
            "*rodando em círculos*",
        ]
        await safe_send(interaction, pick_unique("slash:passear", respostas))
    except Exception as e:
        logger.error(f"Erro no comando /passear: {e}", exc_info=True)
        await safe_send(interaction, "tropecei na guia 🦴", ephemeral=True)


@bot.tree.command(name="truque", description="pede pra kuma fazer um truque")
async def truque(interaction: discord.Interaction):
    """Pede para a Kuma fazer um truque."""
    try:
        if not await guard_slash(interaction):
            return
        truques = [
            "senta! (mas não sentou)",
            "*late pra parede*",
            "*deita no lugar errado*",
            "finge que sabe dar a pata",
            "*rola no chão aleatoriamente*",
            "fica olhando confusa",
            "au? isso era um truque?",
        ]
        await safe_send(interaction, pick_unique("slash:truque", truques))
    except Exception as e:
        logger.error(f"Erro no comando /truque: {e}", exc_info=True)
        await safe_send(interaction, "esqueci o truque 🧠", ephemeral=True)


@bot.tree.command(name="medos", description="lista os medos da kuma")
async def medos(interaction: discord.Interaction):
    """Lista os medos da Kuma."""
    try:
        if not await guard_slash(interaction):
            return
        lista_medos = ", ".join(FEARS)
        await safe_send(interaction, f"tenho medo de: {lista_medos} 😰")
    except Exception as e:
        logger.error(f"Erro no comando /medos: {e}", exc_info=True)
        await safe_send(interaction, "com medo de responder 😨", ephemeral=True)


@bot.tree.command(name="vocabulario", description="mostra quantas palavras a kuma aprendeu")
async def vocabulario(interaction: discord.Interaction):
    """Mostra o vocabulário aprendido."""
    try:
        if not await guard_slash(interaction):
            return
        total = len(learned_words)
        if total == 0:
            nivel = "iniciante"
            frase = "ainda não aprendi nada"
        elif total < 10:
            nivel = "curiosa"
            frase = f"sei {total} palavras (quase nada)"
        elif total < 50:
            nivel = "esperta"
            frase = f"sei {total} palavras! tô ficando esperta"
        else:
            nivel = "gênio canino"
            frase = f"sei {total} palavras!!"

        embed = discord.Embed(
            title="Vocabulário da Kuma",
            description="catálogo premium de latidos e palavras",
        )
        embed.add_field(name="Total", value=f"{total} palavras", inline=True)
        embed.add_field(name="Nível", value=nivel, inline=True)
        embed.add_field(name="Status", value=frase, inline=False)
        if total == 0:
            embed.add_field(name="Palavras", value="(vazio)", inline=False)
        else:
            palavras = sorted(list(learned_words))
            limite = 20
            exibidas = palavras[:limite]
            resto = total - len(exibidas)
            lista = ", ".join(exibidas)
            if resto > 0:
                lista = f"{lista} … (+{resto})"
            embed.add_field(name="Palavras", value=lista, inline=False)
        style_embed(embed, interaction)
        await safe_send(interaction, embed=embed)
    except Exception as e:
        logger.error(f"Erro no comando /vocabulario: {e}", exc_info=True)
        await safe_send(interaction, "esqueci de contar 🔢", ephemeral=True)


@bot.tree.command(name="latir", description="faz a kuma latir")
async def latir(interaction: discord.Interaction):
    """Faz a Kuma latir."""
    try:
        if not await guard_slash(interaction):
            return
        await safe_send(interaction, "au au!")
        await asyncio.sleep(0.5)
        for _ in range(random.randint(2, 4)):
            await send_channel(cast(Messageable, interaction.channel), pick(latidos))
            await asyncio.sleep(0.4)
    except Exception as e:
        logger.error(f"Erro no comando /latir: {e}", exc_info=True)


@bot.tree.command(name="status", description="status completo da kuma")
async def status(interaction: discord.Interaction):
    """Mostra o status completo da Kuma."""
    try:
        if not await guard_slash(interaction):
            return
        mood = time_based_mood()
        vocab = len(learned_words)

        estado = "ofendida 😤" if is_offended() else "de boa"
        poder = "mod ativa 😎" if is_mod() else "cachorra comum"

        embed = discord.Embed(
            title="Status da Kuma",
            description="painel premium do caos canino",
        )
        embed.add_field(name="Humor", value=mood, inline=True)
        embed.add_field(name="Estado", value=estado, inline=True)
        embed.add_field(name="Poder", value=poder, inline=True)
        embed.add_field(name="Vocabulário", value=f"{vocab} palavras", inline=True)
        embed.add_field(name="Resumo", value=f"{mood} • {estado} • {poder}", inline=False)
        style_embed(embed, interaction)

        await safe_send(interaction, embed=embed)
    except Exception as e:
        logger.error(f"Erro no comando /status: {e}", exc_info=True)
        await safe_send(interaction, "não sei meu status 📊", ephemeral=True)


@bot.tree.command(name="desculpa", description="pede desculpas pra kuma")
async def desculpa(interaction: discord.Interaction):
    """Pede desculpas para a Kuma."""
    try:
        if not await guard_slash(interaction):
            return
        if not is_offended():
            await safe_send(interaction, "nem tava brava 🐶")
        else:
            offend(0)
            await safe_send(interaction, "tá bom né... *perdoou mas tá de cara ainda*")
    except Exception as e:
        logger.error(f"Erro no comando /desculpa: {e}", exc_info=True)
        await safe_send(interaction, "ainda tô brava 😤", ephemeral=True)


@bot.tree.command(name="salvar", description="salva manualmente os dados da kuma")
async def salvar(interaction: discord.Interaction):
    """Salva manualmente os dados do bot."""
    try:
        if not await guard_slash(interaction):
            return
        data = export_state()
        save_data(data)
        await safe_send(interaction, "salvei tudo na memória! 🧠💾")
    except Exception as e:
        logger.error(f"Erro no comando /salvar: {e}", exc_info=True)
        await safe_send(interaction, "erro ao salvar... esqueci tudo 😵", ephemeral=True)


@bot.tree.command(name="ajuda", description="lista dos comandos da kuma")
async def ajuda(interaction: discord.Interaction):
    """Lista todos os comandos disponíveis."""
    try:
        if not await guard_slash(interaction):
            return
        embed = discord.Embed(
            title="Comandos da Kuma",
            description="menu principal da spitz do servidor",
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
            ("/salvar", "salva meus dados"),
            ("/ajuda", "essa mensagem"),
        ]

        for cmd, desc in comandos:
            embed.add_field(name=cmd, value=desc, inline=True)

        embed.add_field(
            name="Dica",
            value="me chama de **kuma** nas mensagens e eu respondo",
            inline=False,
        )
        style_embed(embed, interaction)

        await safe_send(interaction, embed=embed)
    except Exception as e:
        logger.error(f"Erro no comando /ajuda: {e}", exc_info=True)
        await safe_send(interaction, "não sei ajudar 😵‍💫", ephemeral=True)


@bot.event
async def on_error(event, *args, **kwargs):
    """Tratamento global de erros."""
    logger.error(f"Erro no evento {event}", exc_info=True)


def run() -> None:
    try:
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            logger.error("DISCORD_TOKEN não encontrado no .env")
            print("❌ Erro: DISCORD_TOKEN não encontrado no arquivo .env")
        else:
            bot.run(token)
    except KeyboardInterrupt:
        logger.info("Bot encerrado pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
    finally:
        try:
            data = export_state()
            save_data(data)
            logger.info("Dados salvos antes do encerramento")
        except Exception as e:
            logger.error(f"Erro ao salvar dados no encerramento: {e}")


if __name__ == "__main__":
    run()




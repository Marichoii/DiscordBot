# -*- coding: utf-8 -*-
from dataclasses import dataclass
import os


@dataclass(frozen=True)
class BotConfig:
    prefix: str = "!"
    autosave_minutes: int = 5
    mod_duration_seconds: int = 10
    offended_duration_seconds: int = 45

    fear_reply: str = "NÃO. MEDO. SOCORRO."

    respond_to_bots_chance: float = 0.3
    bark_burst_chance: float = 0.01
    brainrot_chance: float = 0.02
    kuma_mention_wrong_chance: float = 0.2
    kuma_mention_emoji_chance: float = 0.3
    kuma_recall_wrong_chance: float = 0.3
    kuma_learned_chance: float = 0.1

    on_message_user_cooldown: float = 1.5
    on_message_channel_cooldown: float = 0.4
    slash_user_cooldown: float = 2.0


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


CONFIG = BotConfig(
    prefix=os.getenv("BOT_PREFIX", "!"),
    autosave_minutes=_env_int("AUTOSAVE_MINUTES", 5),
    mod_duration_seconds=_env_int("MOD_DURATION_SECONDS", 10),
    offended_duration_seconds=_env_int("OFFENDED_DURATION_SECONDS", 45),
    respond_to_bots_chance=_env_float("RESPOND_TO_BOTS_CHANCE", 0.3),
    bark_burst_chance=_env_float("BARK_BURST_CHANCE", 0.01),
    brainrot_chance=_env_float("BRAINROT_CHANCE", 0.02),
    kuma_mention_wrong_chance=_env_float("KUMA_WRONG_CHANCE", 0.2),
    kuma_mention_emoji_chance=_env_float("KUMA_EMOJI_CHANCE", 0.3),
    kuma_recall_wrong_chance=_env_float("KUMA_RECALL_WRONG_CHANCE", 0.3),
    kuma_learned_chance=_env_float("KUMA_LEARNED_CHANCE", 0.1),
    on_message_user_cooldown=_env_float("MSG_USER_COOLDOWN", 1.5),
    on_message_channel_cooldown=_env_float("MSG_CHANNEL_COOLDOWN", 0.4),
    slash_user_cooldown=_env_float("SLASH_USER_COOLDOWN", 2.0),
)

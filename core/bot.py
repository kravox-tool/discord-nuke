"""Helpers para crear y ejecutar bots de Discord sin ruido en consola."""

import discord
from discord.ext import commands

from core import ui


def make_bot(prefix="!"):
    intents = discord.Intents.default()
    intents.guilds = True
    intents.guild_messages = True
    intents.members = True
    intents.message_content = True
    return commands.Bot(command_prefix=prefix, intents=intents)


def run_bot(bot, token):
    """Ejecuta el bot. Devuelve True si terminó bien."""
    try:
        bot.run(token, log_handler=None)   # sin logs de discord ensuciando la pantalla
        return True
    except discord.LoginFailure:
        ui.err("Token inválido o expirado.")
    except discord.PrivilegedIntentsRequired:
        ui.err("Activa SERVER MEMBERS y MESSAGE CONTENT en el Developer Portal.")
    except KeyboardInterrupt:
        ui.warn("Interrumpido por el usuario.")
    except Exception as e:
        ui.err(f"Error: {e}")
    return False


async def resolve_guild(bot, guild_id):
    """Busca el servidor en caché y, si no está, lo pide a la API."""
    guild = bot.get_guild(guild_id)
    if guild is not None:
        return guild
    try:
        return await bot.fetch_guild(guild_id)
    except (discord.NotFound, discord.Forbidden):
        return None


def sanitizar_nombre(texto, indice=None):
    txt = texto.strip().lower().replace(" ", "-")
    if indice is not None:
        txt = f"{txt}-{indice:02d}"
    return txt[:100]

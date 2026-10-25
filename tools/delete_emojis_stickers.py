import asyncio

import discord

from core import ui
from core.bot import make_bot, resolve_guild, run_bot

NAME = "Eliminar emojis y stickers"


def run(cfg):
    ui.cabecera("04", "ELIMINAR EMOJIS Y STICKERS")
    guild_id = ui.ask_int("ID del servidor")

    bot = make_bot(prefix=".")
    control = {"listo": False}

    @bot.event
    async def on_ready():
        if control["listo"]:
            return
        control["listo"] = True

        ui.cabecera("04", "ELIMINAR EMOJIS Y STICKERS")
        guild = await resolve_guild(bot, guild_id)
        if guild is None:
            ui.err("El bot no está en ese servidor o la ID es inválida.")
            await bot.close()
            return

        ui.step(f"Servidor: {guild.name} ({guild.id})")

        ui.info("Borrando emojis...")
        try:
            emojis = await guild.fetch_emojis()
        except discord.HTTPException:
            emojis = []

        borrados = 0
        for emoji in emojis:
            try:
                await emoji.delete()
                borrados += 1
                print(f"{ui.GREEN}[+] emoji {emoji.name}{ui.RESET}")
            except discord.HTTPException:
                pass
            await asyncio.sleep(0.2)
        ui.ok(f"Emojis eliminados: {borrados}/{len(emojis)}")

        ui.info("Borrando stickers...")
        try:
            stickers = await guild.fetch_stickers()
        except discord.HTTPException:
            stickers = []

        borrados_st = 0
        for sticker in stickers:
            try:
                await sticker.delete()
                borrados_st += 1
                print(f"{ui.GREEN}[+] sticker {sticker.name}{ui.RESET}")
            except discord.HTTPException:
                pass
            await asyncio.sleep(0.2)
        ui.ok(f"Stickers eliminados: {borrados_st}/{len(stickers)}")

        ui.sep()
        ui.ok("LIMPIEZA COMPLETADA")
        await bot.close()

    run_bot(bot, cfg.token)
    ui.pause()

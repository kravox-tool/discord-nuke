import asyncio

import discord

from core import ui
from core.bot import make_bot, resolve_guild, run_bot

NAME = "Banear a todos los miembros"


def run(cfg):
    ui.cabecera("05", "BANEAR A TODOS LOS MIEMBROS")
    guild_id = ui.ask_int("ID del servidor")
    razon = ui.ask("Razón del ban (ENTER para ninguna)", required=False, default="")
    ignorar_bots = ui.confirm("¿Ignorar cuentas de bots?", default=True)
    retardo = ui.ask_float("Retardo entre bans (seg)", default=0.5, minimum=0)

    bot = make_bot(prefix=".")
    control = {"listo": False}

    @bot.event
    async def on_ready():
        if control["listo"]:
            return
        control["listo"] = True

        ui.cabecera("05", "BANEAR A TODOS LOS MIEMBROS")
        guild = await resolve_guild(bot, guild_id)
        if guild is None:
            ui.err("El bot no está en ese servidor o la ID es inválida.")
            await bot.close()
            return

        ui.step(f"Servidor: {guild.name} ({guild.id})")
        ui.info("Descargando miembros...")
        miembros = [m async for m in guild.fetch_members(limit=None)]
        miembros = [m for m in miembros if m.id != bot.user.id]
        if ignorar_bots:
            miembros = [m for m in miembros if not m.bot]

        if not miembros:
            ui.warn("No hay miembros para banear.")
            await bot.close()
            return

        ui.ok(f"Miembros a banear: {len(miembros)}")
        baneados = 0
        for i, miembro in enumerate(miembros, 1):
            try:
                await guild.ban(miembro, reason=razon or None)
                baneados += 1
                print(f"{ui.GREEN}[{i}/{len(miembros)}] {miembro} baneado{ui.RESET}")
            except discord.Forbidden:
                ui.warn(f"Sin permiso para banear a {miembro}")
            except discord.HTTPException:
                pass
            await asyncio.sleep(retardo)

        ui.sep()
        ui.ok(f"BANEADOS: {baneados}/{len(miembros)}")
        await bot.close()

    run_bot(bot, cfg.token)
    ui.pause()

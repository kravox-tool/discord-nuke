import asyncio

import discord

from core import ui
from core.bot import make_bot, resolve_guild, run_bot

NAME = "DM-SPAM masivo a todo el servidor"


def run(cfg):
    ui.cabecera("06", "DM-SPAM MASIVO")
    guild_id = ui.ask_int("ID del servidor")
    mensaje = ui.ask("Mensaje a enviar por MD")
    cantidad = ui.ask_int("Cantidad de MD por usuario", default=150, minimum=1)
    retardo = ui.ask_float("Retardo entre mensajes (seg)", default=0.7, minimum=0)
    ignorar_bots = ui.confirm("¿Ignorar cuentas de bots?", default=True)

    bot = make_bot(prefix=".")
    control = {"listo": False}

    @bot.event
    async def on_ready():
        if control["listo"]:
            return
        control["listo"] = True

        ui.cabecera("06", "DM-SPAM MASIVO")
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
            ui.warn("No hay miembros a los que escribir.")
            await bot.close()
            return

        ui.ok(f"Usuarios a procesar: {len(miembros)} ({cantidad} MD cada uno)")

        total = 0
        for i, miembro in enumerate(miembros, 1):
            enviados = 0
            for _ in range(cantidad):
                try:
                    await miembro.send(mensaje)
                    enviados += 1
                    total += 1
                except discord.Forbidden:
                    break
                except discord.HTTPException:
                    pass
                await asyncio.sleep(retardo)
            print(f"{ui.GREEN}[{i}/{len(miembros)}]{ui.RESET} {miembro} -> {enviados} MD")

        ui.sep()
        ui.ok(f"MD TOTALES ENVIADOS: {total}")
        await bot.close()

    run_bot(bot, cfg.token)
    ui.pause()

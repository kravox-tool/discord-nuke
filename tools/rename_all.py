import asyncio

import aiohttp
import discord

from core import ui
from core.bot import make_bot, resolve_guild, run_bot, sanitizar_nombre

NAME = "Renombrar todo + nombre e imagen del servidor"


def run(cfg):
    ui.cabecera("07", "RENOMBRAR TODO + SERVIDOR")
    guild_id = ui.ask_int("ID del servidor")
    modo = ui.ask_int(
        "Modo de canales (1 = mismo nombre para todos, 2 = base + número)",
        default=1, minimum=1, maximum=2,
    )
    base = ui.ask("Nombre para los canales" if modo == 1 else "Nombre base para los canales")
    incluir_voz = ui.confirm("¿Renombrar también los canales de voz?", default=True)
    nombre_servidor = ui.ask(
        "Nuevo nombre del servidor (ENTER para no cambiar)", required=False, default=""
    )
    icono_url = ui.ask(
        "URL de imagen para el icono (ENTER para no cambiar)", required=False, default=""
    )

    bot = make_bot(prefix=".")
    control = {"listo": False}

    @bot.event
    async def on_ready():
        if control["listo"]:
            return
        control["listo"] = True

        ui.cabecera("07", "RENOMBRAR TODO + SERVIDOR")
        guild = await resolve_guild(bot, guild_id)
        if guild is None:
            ui.err("El bot no está en ese servidor o la ID es inválida.")
            await bot.close()
            return

        ui.step(f"Servidor: {guild.name} ({guild.id})")

        if nombre_servidor:
            try:
                await guild.edit(name=nombre_servidor)
                ui.ok(f"Nombre del servidor -> {nombre_servidor}")
            except discord.HTTPException:
                ui.warn("No se pudo cambiar el nombre del servidor.")

        if icono_url:
            try:
                async with aiohttp.ClientSession() as s:
                    async with s.get(icono_url) as r:
                        if r.status == 200:
                            await guild.edit(icon=await r.read())
                            ui.ok("Icono del servidor actualizado.")
                        else:
                            ui.warn("No se pudo descargar la imagen.")
            except Exception as e:
                ui.warn(f"Error con el icono: {e}")

        canales = [
            c for c in guild.channels
            if incluir_voz or not isinstance(c, discord.VoiceChannel)
        ]

        ui.info(f"Renombrando {len(canales)} canales...")
        ok_count = 0
        for i, canal in enumerate(canales, 1):
            nuevo = sanitizar_nombre(base, i if modo == 2 else None)
            try:
                await canal.edit(name=nuevo)
                ok_count += 1
                print(f"{ui.GREEN}[{i}/{len(canales)}] {canal.name} -> {nuevo}{ui.RESET}")
            except discord.HTTPException:
                ui.warn(f"No se pudo renombrar {canal.name}")
            await asyncio.sleep(0.3)

        ui.sep()
        ui.ok(f"Canales renombrados: {ok_count}/{len(canales)}")
        await bot.close()

    run_bot(bot, cfg.token)
    ui.pause()

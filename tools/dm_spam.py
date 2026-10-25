import asyncio

import discord

from core import ui
from core.bot import make_bot, run_bot

NAME = "DM-SPAM a un usuario"


def run(cfg):
    ui.cabecera("01", "DM-SPAM A UN USUARIO")
    target_id = ui.ask_int("ID del usuario objetivo")
    mensaje = ui.ask("Mensaje a enviar")
    cantidad = ui.ask_int("Cantidad de mensajes", default=50, minimum=1)
    retardo = ui.ask_float("Retardo entre mensajes (seg)", default=0.7, minimum=0)

    bot = make_bot(prefix=".")
    control = {"listo": False}

    @bot.event
    async def on_ready():
        if control["listo"]:
            return
        control["listo"] = True

        ui.cabecera("01", "DM-SPAM A UN USUARIO")
        ui.info(f"Conectado como {bot.user}")

        try:
            objetivo = await bot.fetch_user(target_id)
        except discord.NotFound:
            ui.err("No existe ningún usuario con esa ID.")
            await bot.close()
            return
        except discord.HTTPException as e:
            ui.err(f"Error consultando la ID: {e}")
            await bot.close()
            return

        ui.sep()
        ui.step(f"Objetivo: {objetivo.name} ({objetivo.id})")
        ui.sep()

        enviados = 0
        for i in range(cantidad):
            try:
                await objetivo.send(mensaje)
                enviados += 1
                print(f"{ui.GREEN}[+] [{enviados}/{cantidad}] enviado{ui.RESET}")
            except discord.Forbidden:
                ui.err("El usuario bloqueó al bot o tiene los MD cerrados.")
                break
            except discord.HTTPException as e:
                ui.warn(f"Fallo el envío {i + 1}: {e}")
            await asyncio.sleep(retardo)

        ui.sep()
        ui.ok(f"Ráfaga finalizada. Total enviados: {enviados}")
        await bot.close()

    run_bot(bot, cfg.token)
    ui.pause()

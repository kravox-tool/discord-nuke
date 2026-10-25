import asyncio

import discord

from core import ui
from core.bot import make_bot, resolve_guild, run_bot, sanitizar_nombre

NAME = "Crear roles / borrar todos los roles"


def run(cfg):
    ui.cabecera("08", "CREAR Y BORRAR ROLES")
    guild_id = ui.ask_int("ID del servidor")
    modo = ui.ask_int(
        "Modo (1 = crear roles, 2 = borrar TODOS los roles, 3 = borrar y luego crear)",
        default=1, minimum=1, maximum=3,
    )

    base = ""
    cantidad = 0
    numerar = False
    color = None

    if modo in (1, 3):
        base = ui.ask("Nombre de los roles")
        cantidad = ui.ask_int("Cantidad de roles a crear", default=10, minimum=1)
        numerar = ui.confirm("¿Añadir numeración al nombre? (ej: nombre-01)", default=True)
        hex_color = ui.ask("Color HEX (ej: ff0000, ENTER para ninguno)", required=False, default="")
        if hex_color:
            try:
                color = discord.Colour.from_str(
                    hex_color if hex_color.startswith("#") else "#" + hex_color
                )
            except ValueError:
                ui.warn("Color inválido, se crearán sin color.")

    borrar = modo in (2, 3)
    crear = modo in (1, 3)

    bot = make_bot(prefix=".")
    control = {"listo": False}

    @bot.event
    async def on_ready():
        if control["listo"]:
            return
        control["listo"] = True

        ui.cabecera("08", "CREAR Y BORRAR ROLES")
        guild = await resolve_guild(bot, guild_id)
        if guild is None:
            ui.err("El bot no está en ese servidor o la ID es inválida.")
            await bot.close()
            return

        ui.step(f"Servidor: {guild.name} ({guild.id})")

        if borrar:
            total = len([r for r in guild.roles if not r.is_default()])
            ui.info(f"Borrando {total} roles...")
            borrados = 0
            for rol in list(guild.roles):
                if rol.is_default():
                    continue
                if rol.managed:
                    ui.warn(f"Saltando rol de bot/integración: {rol.name}")
                    continue
                try:
                    await rol.delete()
                    borrados += 1
                    print(f"{ui.GREEN}[+] borrado {rol.name}{ui.RESET}")
                except discord.HTTPException:
                    pass
                await asyncio.sleep(0.3)
            ui.ok(f"Roles borrados: {borrados}/{total}")

        if crear:
            ui.info("Creando roles...")
            creados = 0
            for i in range(1, cantidad + 1):
                nombre = sanitizar_nombre(base, i if numerar else None)
                try:
                    await guild.create_role(
                        name=nombre,
                        colour=color if color is not None else discord.Colour.default(),
                        mentionable=False,
                        hoist=False,
                    )
                    creados += 1
                    print(f"{ui.GREEN}[+] creado {nombre}{ui.RESET}")
                except discord.HTTPException as e:
                    ui.warn(f"No se pudo crear {nombre}: {e}")
                await asyncio.sleep(0.3)
            ui.ok(f"Roles creados: {creados}/{cantidad}")

        ui.sep()
        ui.ok("OPERACIÓN COMPLETADA")
        await bot.close()

    run_bot(bot, cfg.token)
    ui.pause()

import asyncio

import discord

from core import ui
from core.bot import make_bot, resolve_guild, run_bot

NAME = "Dar un rol a todos los usuarios (admin / sin admin)"


def run(cfg):
    ui.cabecera("09", "DAR ROL A TODOS LOS USUARIOS")
    guild_id = ui.ask_int("ID del servidor")
    modo = ui.ask_int(
        "Modo (1 = rol nuevo CON admin, 2 = rol nuevo SIN admin, 3 = usar rol existente)",
        default=1, minimum=1, maximum=3,
    )

    nombre_rol = ""
    busqueda = ""
    color = None

    if modo == 3:
        busqueda = ui.ask("Nombre o ID del rol existente")
    else:
        nombre_rol = ui.ask("Nombre del rol")
        hex_color = ui.ask("Color HEX (ENTER para ninguno)", required=False, default="")
        if hex_color:
            try:
                color = discord.Colour.from_str(
                    hex_color if hex_color.startswith("#") else "#" + hex_color
                )
            except ValueError:
                ui.warn("Color inválido.")

    ignorar_bots = ui.confirm("¿Ignorar cuentas de bots?", default=True)
    retardo = ui.ask_float("Retardo entre asignaciones (seg)", default=0.4, minimum=0)

    bot = make_bot(prefix=".")
    control = {"listo": False}

    @bot.event
    async def on_ready():
        if control["listo"]:
            return
        control["listo"] = True

        ui.cabecera("09", "DAR ROL A TODOS LOS USUARIOS")
        guild = await resolve_guild(bot, guild_id)
        if guild is None:
            ui.err("El bot no está en ese servidor o la ID es inválida.")
            await bot.close()
            return

        ui.step(f"Servidor: {guild.name} ({guild.id})")

        rol = None
        if modo == 3:
            if busqueda.isdigit():
                rol = guild.get_role(int(busqueda))
            if rol is None:
                for r in guild.roles:
                    if r.name.lower() == busqueda.lower():
                        rol = r
                        break
            if rol is None:
                ui.err("No se encontró ese rol.")
                await bot.close()
                return
            ui.ok(f"Usando rol existente: {rol.name}")
        else:
            permisos = (
                discord.Permissions(administrator=True)
                if modo == 1
                else discord.Permissions.none()
            )
            try:
                rol = await guild.create_role(
                    name=nombre_rol,
                    permissions=permisos,
                    colour=color if color is not None else discord.Colour.default(),
                    hoist=True,
                    mentionable=True,
                )
            except discord.HTTPException as e:
                ui.err(f"No se pudo crear el rol: {e}")
                await bot.close()
                return
            etiqueta = "CON ADMIN" if modo == 1 else "SIN ADMIN"
            ui.ok(f"Rol creado: {rol.name} ({etiqueta})")

        ui.info("Descargando miembros...")
        miembros = [m async for m in guild.fetch_members(limit=None)]
        miembros = [m for m in miembros if m.id != bot.user.id]
        if ignorar_bots:
            miembros = [m for m in miembros if not m.bot]

        if not miembros:
            ui.warn("No hay usuarios a los que dar el rol.")
            await bot.close()
            return

        ui.ok(f"Usuarios a procesar: {len(miembros)}")
        dados = 0
        for i, miembro in enumerate(miembros, 1):
            if rol in miembro.roles:
                continue
            try:
                await miembro.add_roles(rol, reason="Asignación masiva")
                dados += 1
                print(f"{ui.GREEN}[{i}/{len(miembros)}] {miembro}{ui.RESET}")
            except discord.Forbidden:
                ui.warn(f"Sin permiso para {miembro} (rol más alto que el del bot)")
            except discord.HTTPException:
                pass
            await asyncio.sleep(retardo)

        ui.sep()
        ui.ok(f"ROLES ASIGNADOS: {dados}/{len(miembros)}")
        await bot.close()

    run_bot(bot, cfg.token)
    ui.pause()

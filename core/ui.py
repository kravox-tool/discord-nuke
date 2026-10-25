"""Interfaz de consola: colores ANSI, banners, limpieza y helpers de entrada.

Todo pensado para que la pantalla se limpie antes de cada sección y nada
quede acumulado en el terminal (importante en Termux).
"""

import os
import sys

# ------------------------------------------------------------- colores ------
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

WIDTH = 61

# Letras grandes: K V X - N U K E
BANNER = r"""
██╗  ██╗ ██╗   ██╗ ██╗  ██╗      ███╗   ██╗ ██╗   ██╗ ██╗  ██╗
██║ ██╔╝ ██║   ██║ ╚██╗██╔╝      ████╗  ██║ ██║   ██║ ██║ ██╔╝
█████╔╝  ██║   ██║  ╚███╔╝  ████ ██╔██╗ ██║ ██║   ██║ █████╔╝
██╔═██╗  ╚██╗ ██╔╝  ██╔██╗ ╚═══ ██║╚██╗██║ ██║   ██║ ██╔═██╗
██║  ██╗  ╚████╔╝  ██╔╝ ██╗      ██║ ╚████║ ╚██████╔╝ ██║  ██╗
╚═╝  ╚═╝   ╚═══╝   ╚═╝  ╚═╝      ╚═╝  ╚═══╝  ╚═════╝  ╚═╝  ╚═╝
"""


def enable_ansi():
    """Prepara la salida para colores y UTF-8."""
    if os.name == "nt":
        os.system("")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner(subtitle="KVX-NUKE  ·  TERMUX EDITION"):
    print(f"{RED}{BOLD}{BANNER}{RESET}")
    print(f"{RED}{BOLD}{'=' * WIDTH}{RESET}")
    print(f"{CYAN}{BOLD}{subtitle.center(WIDTH)}{RESET}")
    print(f"{RED}{BOLD}{'=' * WIDTH}{RESET}")


def title(text):
    print(f"\n{BLUE}{BOLD}[ {text} ]{RESET}")


def sep(char="=", color=RED):
    print(f"{color}{BOLD}{char * WIDTH}{RESET}")


def ok(msg):
    print(f"{GREEN}{BOLD}[+] {msg}{RESET}")


def err(msg):
    print(f"{RED}{BOLD}[x] {msg}{RESET}")


def warn(msg):
    print(f"{YELLOW}{BOLD}[!] {msg}{RESET}")


def info(msg):
    print(f"{CYAN}[*] {msg}{RESET}")


def step(msg):
    print(f"{YELLOW}[>] {msg}{RESET}")


# ----------------------------------------------------------- entradas -------
def ask(label, default=None, required=True):
    while True:
        extra = f" {DIM}(ENTER = {default}){RESET}" if default is not None else ""
        raw = input(f"{GREEN}  -> {label}{RESET}{extra}: ").strip()
        if not raw:
            if default is not None:
                return default
            if not required:
                return ""
            err("Este campo no puede estar vacío.")
            continue
        return raw


def ask_int(label, default=None, minimum=None, maximum=None):
    while True:
        raw = ask(label, default=None if default is None else str(default))
        try:
            valor = int(raw)
        except ValueError:
            err("Debe ser un número entero.")
            continue
        if minimum is not None and valor < minimum:
            err(f"El mínimo es {minimum}.")
            continue
        if maximum is not None and valor > maximum:
            err(f"El máximo es {maximum}.")
            continue
        return valor


def ask_float(label, default=None, minimum=None):
    while True:
        raw = ask(label, default=None if default is None else str(default))
        try:
            valor = float(raw.replace(",", "."))
        except ValueError:
            err("Debe ser un número (ej: 0.7).")
            continue
        if minimum is not None and valor < minimum:
            err(f"El mínimo es {minimum}.")
            continue
        return valor


def confirm(label, default=True):
    opciones = "S/n" if default else "s/N"
    while True:
        raw = input(f"{GREEN}  -> {label} [{opciones}]: {RESET}").strip().lower()
        if not raw:
            return default
        if raw in ("s", "si", "sí", "y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        err("Responde 's' o 'n'.")


def pause(msg="Presiona ENTER para volver al menú..."):
    try:
        input(f"\n{YELLOW}{msg}{RESET}")
    except KeyboardInterrupt:
        pass


def cabecera(numero, nombre):
    clear()
    banner(f"{numero} · {nombre}")

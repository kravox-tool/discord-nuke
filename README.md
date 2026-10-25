# Discord Termux Tools

Panel de consola en Python con menú numerado (01-07) para automatizar tareas
de Discord desde Termux. Pantalla limpia, banners ASCII y cero basura acumulada.

## Herramientas

| # | Herramienta |
|---|-------------|
| 01 | DM-SPAM a un usuario |
| 02 | Auto-Nuke de servidor (al entrar) |
| 03 | Nuke por comando `!nuke` |
| 04 | Eliminar todos los emojis y stickers |
| 05 | Banear a todos los miembros |
| 06 | DM-SPAM masivo a todo el servidor (cantidad configurable, 150 por defecto) |
| 07 | Renombrar todos los canales + cambiar nombre e imagen del servidor |

## Instalación en Termux

```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/TU_USUARIO/discord-termux-tools.git
cd discord-termux-tools
pip install -r requirements.txt
bash run.sh

"""Configuración global del panel."""


class Config:
    def __init__(self):
        self.token = ""
        # IDs de servidores que nunca deben ser nukeados
        self.protected_ids = ["1524449604446322708"]

    def es_protegida(self, guild_id):
        return str(guild_id) in self.protected_ids


CONFIG = Config()

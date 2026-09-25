from typing import Dict, Any


class Usuario:
    """Representa un usuario registrado en el sistema."""

    def __init__(self, usuario_id: str, nombre: str, rol: str = "Cliente") -> None:
        self.usuario_id: str = str(usuario_id).strip()
        self.nombre: str = nombre.strip()
        self.rol: str = rol.strip()

    def a_diccionario(self) -> Dict[str, Any]:
        return {"usuario_id": self.usuario_id, "nombre": self.nombre, "rol": self.rol}

    def __str__(self) -> str:
        return f"[{self.usuario_id}] {self.nombre} - Rol: {self.rol}"

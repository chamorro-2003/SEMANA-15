from datetime import datetime
from typing import Dict, Any, Optional


class Venta:
    """Clase entidad que representa una transacción de venta realizada en el restaurante."""

    def __init__(
        self,
        venta_id: int,
        usuario_id: str,
        nombre_usuario: str,
        producto_id: int,
        nombre_producto: str,
        precio: float,
        fecha: Optional[str] = None,
    ) -> None:
        self.venta_id: int = int(venta_id)
        self.usuario_id: str = str(usuario_id).strip()
        self.nombre_usuario: str = nombre_usuario.strip()
        self.producto_id: int = int(producto_id)
        self.nombre_producto: str = nombre_producto.strip()
        self.precio: float = float(precio)
        self.fecha: str = (
            fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    def a_diccionario(self) -> Dict[str, Any]:
        return {
            "venta_id": self.venta_id,
            "usuario_id": self.usuario_id,
            "nombre_usuario": self.nombre_usuario,
            "producto_id": self.producto_id,
            "nombre_producto": self.nombre_producto,
            "precio": self.precio,
            "fecha": self.fecha,
        }

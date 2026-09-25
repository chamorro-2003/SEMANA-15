from typing import Dict, Any


class Producto:
    """Representa un producto del menú o inventario del restaurante."""

    def __init__(
        self,
        producto_id: int,
        nombre: str,
        precio: float,
        categoria: str,
        stock: int = 0,
    ) -> None:
        self.producto_id: int = int(producto_id)
        self.nombre: str = nombre.strip()
        self.precio: float = float(precio)
        self.categoria: str = categoria.strip()
        self.stock: int = int(stock)

    def a_diccionario(self) -> Dict[str, Any]:
        return {
            "producto_id": self.producto_id,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "stock": self.stock,
        }

    def __str__(self) -> str:
        return f"[{self.producto_id}] {self.nombre} - ${self.precio:.2f} ({self.categoria}) - Stock: {self.stock}"

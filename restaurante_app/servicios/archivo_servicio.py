import json
import os
from typing import List
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:
    """Encargado de la persistencia de datos mediante archivos JSON."""

    def __init__(self, carpeta_datos: str = "datos") -> None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.carpeta_datos = os.path.join(base_dir, carpeta_datos)
        self.ruta_productos: str = os.path.join(self.carpeta_datos, "productos.json")
        self.ruta_usuarios: str = os.path.join(self.carpeta_datos, "usuarios.json")
        self.ruta_ventas: str = os.path.join(self.carpeta_datos, "ventas.json")
        self._asegurar_directorio()

    def _asegurar_directorio(self) -> None:
        """Crea el directorio de datos si no existe."""
        if not os.path.exists(self.carpeta_datos):
            os.makedirs(self.carpeta_datos)

    def cargar_productos(self) -> List[Producto]:
        productos: List[Producto] = []
        try:
            with open(self.ruta_productos, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for item in datos:
                    productos.append(
                        Producto(
                            producto_id=item["producto_id"],
                            nombre=item["nombre"],
                            precio=item["precio"],
                            categoria=item["categoria"],
                            stock=item.get("stock", 0),
                        )
                    )
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return productos

    def guardar_productos(self, productos: List[Producto]) -> None:
        datos = [p.a_diccionario() for p in productos]
        with open(self.ruta_productos, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def cargar_usuarios(self) -> List[Usuario]:
        usuarios: List[Usuario] = []
        try:
            with open(self.ruta_usuarios, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for item in datos:
                    usuarios.append(
                        Usuario(
                            usuario_id=item["usuario_id"],
                            nombre=item["nombre"],
                            rol=item.get("rol", "Cliente"),
                        )
                    )
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return usuarios

    def cargar_ventas(self) -> List[Venta]:
        ventas: List[Venta] = []
        try:
            with open(self.ruta_ventas, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for item in datos:
                    ventas.append(
                        Venta(
                            venta_id=item["venta_id"],
                            usuario_id=item["usuario_id"],
                            nombre_usuario=item["nombre_usuario"],
                            producto_id=item["producto_id"],
                            nombre_producto=item["nombre_producto"],
                            precio=item["precio"],
                            fecha=item.get("fecha"),
                        )
                    )
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return ventas

    def guardar_ventas(self, ventas: List[Venta]) -> None:
        datos = [v.a_diccionario() for v in ventas]
        with open(self.ruta_ventas, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

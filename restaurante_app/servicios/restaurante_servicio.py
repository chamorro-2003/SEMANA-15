from typing import List, Tuple, Optional
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """Lógica de negocio, autenticación, operaciones CRUD y procesamiento de ventas."""

    def __init__(self, archivo_servicio: ArchivoServicio) -> None:
        self.archivo_servicio = archivo_servicio
        self.productos: List[Producto] = self.archivo_servicio.cargar_productos()
        self.usuarios: List[Usuario] = self.archivo_servicio.cargar_usuarios()
        self.ventas: List[Venta] = self.archivo_servicio.cargar_ventas()
        self.usuario_actual: Optional[Usuario] = None

    def validar_acceso(self, usuario_id: str, clave: str) -> bool:
        u_id = usuario_id.strip()
        pwd = clave.strip()

        if not u_id or not pwd:
            return False

        # Caso especial para superadministrador por defecto
        if u_id == "admin" and pwd == "admin":
            self.usuario_actual = Usuario(
                usuario_id="admin",
                nombre="Administrador Principal",
                rol="Administrador",
            )
            return True

        # Búsqueda en la lista de usuarios
        usuario_encontrado = next(
            (u for u in self.usuarios if str(u.usuario_id).strip() == u_id), None
        )
        if usuario_encontrado:
            self.usuario_actual = usuario_encontrado
            return True

        return False

    def obtener_usuario_actual(self) -> Optional[Usuario]:
        return self.usuario_actual

    def cerrar_sesion(self) -> None:
        self.usuario_actual = None

    def obtener_usuarios(self) -> List[Usuario]:
        return self.usuarios

    def obtener_productos(self) -> List[Producto]:
        return self.productos

    def obtener_ventas(self) -> List[Venta]:
        return self.ventas

    def agregar_producto(
        self, p_id: int, nombre: str, precio: float, categoria: str, stock: int
    ) -> bool:
        if any(p.producto_id == p_id for p in self.productos):
            return False
        nuevo = Producto(p_id, nombre, precio, categoria, stock)
        self.productos.append(nuevo)
        self.archivo_servicio.guardar_productos(self.productos)
        return True

    def actualizar_producto(
        self, p_id: int, nombre: str, precio: float, categoria: str, stock: int
    ) -> bool:
        for p in self.productos:
            if p.producto_id == p_id:
                p.nombre = nombre.strip()
                p.precio = float(precio)
                p.categoria = categoria.strip()
                p.stock = int(stock)
                self.archivo_servicio.guardar_productos(self.productos)
                return True
        return False

    def eliminar_producto(self, p_id: int) -> bool:
        for p in self.productos:
            if p.producto_id == p_id:
                self.productos.remove(p)
                self.archivo_servicio.guardar_productos(self.productos)
                return True
        return False

    def registrar_venta(self, usuario_id: str, producto_id: int) -> Tuple[bool, str]:
        usuario = next((u for u in self.usuarios if u.usuario_id == usuario_id), None)
        if not usuario and usuario_id == "admin":
            usuario = self.usuario_actual

        if not usuario:
            return False, "El usuario seleccionado no existe."

        producto = next(
            (p for p in self.productos if p.producto_id == producto_id), None
        )
        if not producto:
            return False, "El producto seleccionado no existe."

        if producto.stock <= 0:
            return False, f"El producto '{producto.nombre}' no tiene stock disponible."

        producto.stock -= 1
        self.archivo_servicio.guardar_productos(self.productos)

        nuevo_id = len(self.ventas) + 1
        nueva_venta = Venta(
            venta_id=nuevo_id,
            usuario_id=usuario.usuario_id,
            nombre_usuario=usuario.nombre,
            producto_id=producto.producto_id,
            nombre_producto=producto.nombre,
            precio=producto.precio,
        )

        self.ventas.append(nueva_venta)
        self.archivo_servicio.guardar_ventas(self.ventas)
        return True, f"Venta #{nuevo_id} registrada con éxito."

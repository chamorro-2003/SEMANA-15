import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Union
from servicios.restaurante_servicio import RestauranteServicio


class MainView(ttk.Frame):
    """Panel principal con vistas condicionadas según el rol del usuario."""

    def __init__(
        self,
        parent: Union[tk.Tk, tk.Widget],
        servicio: RestauranteServicio,
        on_logout: Callable,
    ) -> None:
        super().__init__(parent, padding=10)
        self.servicio = servicio
        self.on_logout = on_logout
        self.dict_usuarios = {}
        self.dict_productos = {}

        self._cargar_recursos_visuales()
        self._crear_interfaz()

    def _cargar_recursos_visuales(self) -> None:
        """Carga los iconos desde la carpeta assets/."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ruta_assets = os.path.join(base_dir, "assets")

        def _cargar_img(nombre_archivo: str) -> Union[tk.PhotoImage, None]:
            ruta = os.path.join(self.ruta_assets, nombre_archivo)
            return tk.PhotoImage(file=ruta) if os.path.exists(ruta) else None

        self.img_logo = _cargar_img("logo.png")
        self.img_icon_venta = _cargar_img("icon_venta.png")
        self.img_icon_producto = _cargar_img("icon_producto.png")
        self.img_icon_usuario = _cargar_img("icon_usuario.png")

    def inicializar_vista(self) -> None:
        """Reconstruye los elementos de la interfaz al iniciar sesión según el rol."""
        for widget in self.winfo_children():
            widget.destroy()
        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        usuario = self.servicio.obtener_usuario_actual()
        rol = usuario.rol if usuario else "Cliente"
        nombre_usr = usuario.nombre if usuario else "Usuario"

        # Encabezado
        frame_top = ttk.Frame(self)
        frame_top.pack(fill="x", pady=5)

        if self.img_logo:
            lbl_logo = ttk.Label(frame_top, image=self.img_logo)
            lbl_logo.pack(side="left", padx=(0, 10))

        frame_titulos = ttk.Frame(frame_top)
        frame_titulos.pack(side="left")

        ttk.Label(
            frame_titulos,
            text="Sistema de Gestión de Restaurante",
            font=("Arial", 13, "bold"),
        ).pack(anchor="w")

        ttk.Label(
            frame_titulos,
            text=f"Sesión activa: {nombre_usr} ({rol})",
            font=("Arial", 9, "italic"),
            foreground="#555555",
        ).pack(anchor="w")

        ttk.Button(frame_top, text="Cerrar Sesión", command=self.on_logout).pack(
            side="right"
        )

        # Pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, pady=10)

        # Pestaña Registro de Ventas
        tab_ventas = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_ventas, text=" Registro de Ventas")
        if self.img_icon_venta:
            self.notebook.tab(tab_ventas, image=self.img_icon_venta, compound="left")
        self._construir_pestana_ventas(tab_ventas)

        # Pestañas adicionales solo para administradores
        if rol == "Administrador":

            # Pestaña Gestión de Productos
            tab_productos = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(tab_productos, text=" Gestión de Productos")
            if self.img_icon_producto:
                self.notebook.tab(
                    tab_productos, image=self.img_icon_producto, compound="left"
                )
            self._construir_pestana_productos(tab_productos)

            # Pestaña Consulta de Usuarios
            tab_usuarios = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(tab_usuarios, text=" Consulta de Usuarios")
            if self.img_icon_usuario:
                self.notebook.tab(
                    tab_usuarios, image=self.img_icon_usuario, compound="left"
                )
            self._construir_pestana_usuarios(tab_usuarios)

    def _construir_pestana_ventas(self, parent: ttk.Frame) -> None:
        f_form = ttk.LabelFrame(parent, text=" Nueva Operación de Venta ", padding=10)
        f_form.pack(fill="x", pady=5)

        ttk.Label(f_form, text="Cliente:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.cb_usuarios = ttk.Combobox(f_form, state="readonly", width=28)
        self.cb_usuarios.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(f_form, text="Producto:").grid(
            row=0, column=2, padx=5, pady=5, sticky="e"
        )
        self.cb_productos = ttk.Combobox(f_form, state="readonly", width=30)
        self.cb_productos.grid(row=0, column=3, padx=5, pady=5)

        btn_kwargs = {
            "text": " Registrar Venta",
            "command": self._callback_registrar_venta,
        }
        if self.img_icon_venta:
            btn_kwargs["image"] = self.img_icon_venta
            btn_kwargs["compound"] = "left"

        btn_venta = ttk.Button(f_form, **btn_kwargs)
        btn_venta.grid(row=0, column=4, padx=15, pady=5)

        f_tabla = ttk.LabelFrame(parent, text=" Historial de Ventas ", padding=10)
        f_tabla.pack(fill="both", expand=True, pady=5)

        self.tabla_ventas = ttk.Treeview(
            f_tabla,
            columns=("ID", "Usuario", "Producto", "Precio", "Fecha"),
            show="headings",
        )
        self.tabla_ventas.heading("ID", text="ID")
        self.tabla_ventas.heading("Usuario", text="Cliente")
        self.tabla_ventas.heading("Producto", text="Producto")
        self.tabla_ventas.heading("Precio", text="Precio ($)")
        self.tabla_ventas.heading("Fecha", text="Fecha y Hora")

        self.tabla_ventas.column("ID", width=40, anchor="center")
        self.tabla_ventas.column("Usuario", width=160)
        self.tabla_ventas.column("Producto", width=160)
        self.tabla_ventas.column("Precio", width=80, anchor="e")
        self.tabla_ventas.column("Fecha", width=140, anchor="center")

        self.tabla_ventas.pack(fill="both", expand=True)

        self._actualizar_desplegables_ventas()
        self._cargar_tabla_ventas()

    def _actualizar_desplegables_ventas(self) -> None:
        usuarios = self.servicio.obtener_usuarios()
        self.dict_usuarios = {
            f"{u.nombre} ({u.usuario_id})": u.usuario_id for u in usuarios
        }
        self.cb_usuarios["values"] = list(self.dict_usuarios.keys())

        productos = self.servicio.obtener_productos()
        self.dict_productos = {
            f"{p.nombre} - ${p.precio:.2f} (Stock: {p.stock})": p.producto_id
            for p in productos
        }
        self.cb_productos["values"] = list(self.dict_productos.keys())

    def _cargar_tabla_ventas(self) -> None:
        for row in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(row)
        for v in self.servicio.obtener_ventas():
            self.tabla_ventas.insert(
                "",
                "end",
                values=(
                    v.venta_id,
                    v.nombre_usuario,
                    v.nombre_producto,
                    f"{v.precio:.2f}",
                    v.fecha,
                ),
            )

    def _callback_registrar_venta(self) -> None:
        usr_sel = self.cb_usuarios.get()
        prod_sel = self.cb_productos.get()

        if not usr_sel or not prod_sel:
            messagebox.showwarning(
                "Atención", "Debe seleccionar un usuario y un producto."
            )
            return

        usr_id = self.dict_usuarios[usr_sel]
        prod_id = self.dict_productos[prod_sel]

        exito, msj = self.servicio.registrar_venta(usr_id, prod_id)

        if exito:
            messagebox.showinfo("Éxito", msj)
            self._actualizar_desplegables_ventas()
            self._cargar_tabla_ventas()
            if hasattr(self, "tabla_prod"):
                self._cargar_tabla_productos()
            self.cb_usuarios.set("")
            self.cb_productos.set("")
        else:
            messagebox.showerror("Error", msj)

    def _construir_pestana_productos(self, parent: ttk.Frame) -> None:
        f_form = ttk.LabelFrame(parent, text=" Formulario de Producto ", padding=10)
        f_form.pack(fill="x", pady=5)

        ttk.Label(f_form, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ent_id = ttk.Entry(f_form, width=8)
        self.ent_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(f_form, text="Nombre:").grid(
            row=0, column=2, padx=5, pady=5, sticky="e"
        )
        self.ent_nombre = ttk.Entry(f_form, width=20)
        self.ent_nombre.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(f_form, text="Precio:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.ent_precio = ttk.Entry(f_form, width=8)
        self.ent_precio.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(f_form, text="Categoría:").grid(
            row=1, column=2, padx=5, pady=5, sticky="e"
        )
        self.ent_categoria = ttk.Entry(f_form, width=20)
        self.ent_categoria.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(f_form, text="Stock:").grid(
            row=0, column=4, padx=5, pady=5, sticky="e"
        )
        self.ent_stock = ttk.Entry(f_form, width=8)
        self.ent_stock.grid(row=0, column=5, padx=5, pady=5)

        f_botones = ttk.Frame(parent)
        f_botones.pack(fill="x", pady=5)

        ttk.Button(f_botones, text="Registrar", command=self._registrar_prod).pack(
            side="left", padx=5
        )
        ttk.Button(f_botones, text="Actualizar", command=self._actualizar_prod).pack(
            side="left", padx=5
        )
        ttk.Button(f_botones, text="Eliminar", command=self._eliminar_prod).pack(
            side="left", padx=5
        )
        ttk.Button(f_botones, text="Limpiar Campos", command=self._limpiar_campos).pack(
            side="left", padx=5
        )

        f_tabla = ttk.LabelFrame(parent, text=" Productos Registrados ", padding=10)
        f_tabla.pack(fill="both", expand=True, pady=5)

        self.tabla_prod = ttk.Treeview(
            f_tabla,
            columns=("ID", "Nombre", "Precio", "Categoría", "Stock"),
            show="headings",
        )
        self.tabla_prod.heading("ID", text="ID")
        self.tabla_prod.heading("Nombre", text="Nombre")
        self.tabla_prod.heading("Precio", text="Precio ($)")
        self.tabla_prod.heading("Categoría", text="Categoría")
        self.tabla_prod.heading("Stock", text="Stock")

        self.tabla_prod.column("ID", width=50, anchor="center")
        self.tabla_prod.column("Nombre", width=180)
        self.tabla_prod.column("Precio", width=70, anchor="e")
        self.tabla_prod.column("Categoría", width=110)
        self.tabla_prod.column("Stock", width=60, anchor="center")

        self.tabla_prod.pack(fill="both", expand=True)
        self.tabla_prod.bind("<<TreeviewSelect>>", self._seleccionar_producto)

        self._cargar_tabla_productos()

    def _cargar_tabla_productos(self) -> None:
        for row in self.tabla_prod.get_children():
            self.tabla_prod.delete(row)
        for p in self.servicio.obtener_productos():
            self.tabla_prod.insert(
                "",
                "end",
                values=(
                    p.producto_id,
                    p.nombre,
                    f"{p.precio:.2f}",
                    p.categoria,
                    p.stock,
                ),
            )

    def _registrar_prod(self) -> None:
        try:
            p_id = int(self.ent_id.get().strip())
            nombre = self.ent_nombre.get().strip()
            precio = float(self.ent_precio.get().strip())
            categoria = self.ent_categoria.get().strip()
            stock = int(self.ent_stock.get().strip())

            if not nombre or not categoria:
                messagebox.showwarning("Atención", "Complete todos los campos.")
                return

            if self.servicio.agregar_producto(p_id, nombre, precio, categoria, stock):
                self._cargar_tabla_productos()
                self._actualizar_desplegables_ventas()
                self._limpiar_campos()
                messagebox.showinfo("Éxito", "Producto registrado correctamente.")
            else:
                messagebox.showerror("Error", "El ID de producto ya existe.")
        except ValueError:
            messagebox.showerror(
                "Error", "Asegúrese de ingresar ID, Precio y Stock válidos."
            )

    def _actualizar_prod(self) -> None:
        try:
            p_id = int(self.ent_id.get().strip())
            nombre = self.ent_nombre.get().strip()
            precio = float(self.ent_precio.get().strip())
            categoria = self.ent_categoria.get().strip()
            stock = int(self.ent_stock.get().strip())

            if self.servicio.actualizar_producto(
                p_id, nombre, precio, categoria, stock
            ):
                self._cargar_tabla_productos()
                self._actualizar_desplegables_ventas()
                self._limpiar_campos()
                messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            else:
                messagebox.showerror(
                    "Error", "No existe un producto registrado con ese ID."
                )
        except ValueError:
            messagebox.showerror(
                "Error", "Asegúrese de que los datos numéricos sean válidos."
            )

    def _eliminar_prod(self) -> None:
        try:
            p_id = int(self.ent_id.get().strip())
            if self.servicio.eliminar_producto(p_id):
                self._cargar_tabla_productos()
                self._actualizar_desplegables_ventas()
                self._limpiar_campos()
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se encontró un producto con ese ID.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un ID de producto válido.")

    def _seleccionar_producto(self, event) -> None:
        item = self.tabla_prod.focus()
        if item:
            val = self.tabla_prod.item(item, "values")
            self.ent_id.delete(0, tk.END)
            self.ent_id.insert(0, val[0])
            self.ent_nombre.delete(0, tk.END)
            self.ent_nombre.insert(0, val[1])
            self.ent_precio.delete(0, tk.END)
            self.ent_precio.insert(0, val[2])
            self.ent_categoria.delete(0, tk.END)
            self.ent_categoria.insert(0, val[3])
            self.ent_stock.delete(0, tk.END)
            self.ent_stock.insert(0, val[4])

    def _limpiar_campos(self) -> None:
        self.ent_id.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_precio.delete(0, tk.END)
        self.ent_categoria.delete(0, tk.END)
        self.ent_stock.delete(0, tk.END)

    def _construir_pestana_usuarios(self, parent: ttk.Frame) -> None:
        f_tabla = ttk.LabelFrame(
            parent, text=" Lista de Usuarios Registrados ", padding=10
        )
        f_tabla.pack(fill="both", expand=True)

        tabla_usr = ttk.Treeview(
            f_tabla, columns=("ID", "Nombre", "Rol"), show="headings"
        )
        tabla_usr.heading("ID", text="Cédula / ID")
        tabla_usr.heading("Nombre", text="Nombre Completo")
        tabla_usr.heading("Rol", text="Rol de Usuario")

        tabla_usr.column("ID", width=120, anchor="center")
        tabla_usr.column("Nombre", width=220)
        tabla_usr.column("Rol", width=100, anchor="center")

        tabla_usr.pack(fill="both", expand=True)

        for u in self.servicio.obtener_usuarios():
            tabla_usr.insert("", "end", values=(u.usuario_id, u.nombre, u.rol))

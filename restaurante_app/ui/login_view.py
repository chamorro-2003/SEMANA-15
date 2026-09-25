import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Union
from servicios.restaurante_servicio import RestauranteServicio


class LoginView(ttk.Frame):
    """Pantalla para el inicio de sesión del sistema."""

    def __init__(
        self,
        parent: Union[tk.Tk, tk.Widget],
        servicio: RestauranteServicio,
        on_login_success: Callable,
    ) -> None:
        super().__init__(parent, padding=20)
        self.servicio = servicio
        self.on_login_success = on_login_success
        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        card = ttk.LabelFrame(self, text=" Acceso al Sistema Restaurante ", padding=20)
        card.pack(expand=True)

        ttk.Label(card, text="ID Usuario:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.entry_usuario = ttk.Entry(card, width=25)
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(card, text="Contraseña:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.entry_clave = ttk.Entry(card, width=25, show="*")
        self.entry_clave.grid(row=1, column=1, padx=5, pady=5)

        # Evento command -> callback _procesar_login
        btn_ingresar = ttk.Button(card, text="Ingresar", command=self._procesar_login)
        btn_ingresar.grid(row=2, column=0, columnspan=2, pady=15)

    def _procesar_login(self) -> None:
        usuario_id = self.entry_usuario.get().strip()
        clave = self.entry_clave.get().strip()

        if not usuario_id or not clave:
            messagebox.showwarning("Atención", "Por favor, complete todos los campos.")
            return

        if self.servicio.validar_acceso(usuario_id, clave):
            self.entry_usuario.delete(0, tk.END)
            self.entry_clave.delete(0, tk.END)
            self.on_login_success()
        else:
            messagebox.showerror(
                "Error de Acceso", "Credenciales incorrectas o usuario no registrado."
            )

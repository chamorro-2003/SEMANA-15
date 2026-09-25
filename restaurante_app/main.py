import os
import tkinter as tk
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class AplicacionPrincipal:
    """Orquestador principal de la aplicación."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Restaurante")
        self.root.geometry("820x580")

        # Configuración del icono .ico para la ventana principal
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ico_path = os.path.join(base_dir, "assets", "app_icon.ico")
        if os.path.exists(ico_path):
            try:
                self.root.iconbitmap(ico_path)
            except Exception:
                pass

        # Inicialización de servicios
        self.archivo_servicio = ArchivoServicio()
        self.restaurante_servicio = RestauranteServicio(self.archivo_servicio)

        # Creación de vistas
        self.login_view = LoginView(
            self.root, self.restaurante_servicio, self.mostrar_main
        )
        self.main_view = MainView(
            self.root, self.restaurante_servicio, self.cerrar_sesion
        )

        self.mostrar_login()

    def mostrar_login(self) -> None:
        self.main_view.pack_forget()
        self.login_view.pack(fill="both", expand=True)

    def mostrar_main(self) -> None:
        self.login_view.pack_forget()
        self.main_view.inicializar_vista()
        self.main_view.pack(fill="both", expand=True)

    def cerrar_sesion(self) -> None:
        self.restaurante_servicio.cerrar_sesion()
        self.mostrar_login()

    def ejecutar(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = AplicacionPrincipal()
    app.ejecutar()

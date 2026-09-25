<div align="justify">
  
# RESTURANTE_SEMANA_14

# Universidad Estatal Amazonica (UEA)

# Sistema de Gestión de Restaurante - Componentes y Contenedores en Tkinter

**Estudiante:** Nayely Soledad Chamorro Vicente

**Asignatura:** Programación Orientada a Objetos

---

## Descripción General del Sistema

Este proyecto es una aplicación de escritorio desarrollada en Python y Tkinter que permite gestionar diferentes operaciones de un restaurante mediante una interfaz gráfica organizada, incorporando el registro de productos, usuarios y ventas, además del control de acceso según el rol de cada usuario, de esta manera los administradores pueden gestionar el catálogo y consultar usuarios, mientras que los clientes cuentan con acceso al módulo de ventas, asimismo la información se mantiene almacenada mediante archivos **JSON** para conservar los datos entre diferentes ejecuciones del sistema.

---

## Estructura del Proyecto

El sistema mantiene una organización modular que permite separar las responsabilidades de cada componente, donde la carpeta **assets/** contiene los recursos gráficos utilizados en la interfaz, **datos/** almacena la información persistente de productos, usuarios y ventas, **modelos/** contiene las entidades principales, **servicios/** administra la lógica de negocio y persistencia, mientras que **ui/** contiene las vistas gráficas desarrolladas con **Tkinter**, finalmente **main.py** funciona como punto de entrada y coordina la ejecución de la aplicación.

```text
restaurante_app/
│
├── assets/
│   ├── app_icon.ico
│   ├── logo.png
│   ├── icon_producto.png
│   ├── icon_usuario.png
│   └── icon_venta.png
│
├── datos/
│   ├── productos.json
│   └── usuarios.json
│   └── ventas.json
│
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
│
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
│
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
│
├── main.py
└── README.md
```

---
## Componentes Técnicos Aplicados
---

## Responsabilidad de las Clases y Módulos

Cada componente cumple una función específica dentro del sistema, por lo que las clases **Producto**, **Usuario** y **Venta** representan las entidades principales y contienen la información necesaria para su funcionamiento, mientras que **archivo_servicio.py** administra la lectura, escritura y conversión de los datos almacenados en archivos **JSON**, por otra parte, **restaurante_servicio.py** concentra las reglas de negocio, el control del stock, las ventas y la autenticación de usuarios, finalmente **login_view.py** controla el acceso y **main_view.py** presenta el panel principal de acuerdo con el rol del usuario autenticado.

---

## Control de Acceso por Roles

El sistema incorpora un mecanismo de control de acceso basado en **roles (RBAC)** que determina las funciones disponibles después del inicio de sesión, de manera que los usuarios con rol de **Administrador** pueden acceder a la gestión de productos, consulta de usuarios y registro de ventas, mientras que los usuarios regulares tienen acceso únicamente al módulo de ventas, para ello **MainView** comprueba el rol del usuario antes de crear las diferentes pestañas del sistema, evitando que las opciones restringidas sean mostradas a quienes no cuentan con la autorización correspondiente.

---

## Persistencia y Gestión de Ventas

La información del sistema se mantiene mediante tres archivos **JSON**, donde **productos.json* almacena el catálogo y el stock disponible, **usuarios.json** conserva los datos de clientes y administradores, *ventas.json** registra las transacciones realizadas, además cuando se procesa una venta el sistema verifica que el producto exista y que tenga suficiente stock, posteriormente disminuye las unidades disponibles y guarda los cambios correspondientes, permitiendo que la información permanezca actualizada incluso después de cerrar y volver a ejecutar la aplicación.

---

## Reflexión Final

El desarrollo de EV15 permitió integrar los conocimientos adquiridos durante las diferentes etapas del proyecto, combinando **Programación Orientada a Objetos**, **interfaces gráficas**, persistencia de datos y control de acceso para construir una aplicación más completa y organizada, además la separación entre modelos, servicios e interfaz facilita el mantenimiento del código y permite incorporar nuevas funciones sin afectar directamente las demás partes del sistema, de esta manera el proyecto establece una base adecuada para continuar mejorando la aplicación mediante nuevas opciones de gestión, reportes o diferentes formas de almacenamiento de información.

<div>

# Inventory Management System 🍦

Sistema web de gestión de inventario y control de stock desarrollado con Flask, MySQL y JavaScript vanilla. Permite administrar productos, categorías, usuarios y registrar el historial de movimientos en tiempo real desde una interfaz web moderna y responsiva.

## 🚀 Descripción general

Este proyecto es un MVP (Mínimo Viable Producto) diseñado para resolver la gestión de inventario de un negocio real (como una heladería). No solo permite el clásico ABM (CRUD) de productos, sino que también integra un sistema de seguridad con sesiones y un registro automatizado de auditoría para cada entrada y salida de mercancía.

## 🛠️ Tecnologías utilizadas

- **Backend:** Python 3 (Flask, Jinja2, PyMySQL)
- **Seguridad:** Werkzeug (Encriptación de contraseñas con Hash)
- **Base de Datos:** MySQL (Alojada en la nube con **Aiven**)
- **Frontend:** HTML5, CSS3 (Diseño responsivo Dark Mode)
- **Despliegue:** **Render** (Alojamiento del servicio web de Flask)

## 📁 Estructura del proyecto

```text
inventory-management-system/
├── app.py
├── database.sql
├── README.md
├── modulos/
│   ├── __init__.py
│   ├── comandos_db_producto.py
│   └── conexion.py
├── static/
│   ├── css/
│   └── js/
└── templates/
    ├── index.html            # Dashboard con alertas de stock crítico
    ├── login.html            # Pantalla de acceso seguro
    ├── registro.html         # Registro de nuevos empleados
    ├── productos.html        # Listado, acciones rápidas e incremento de stock
    ├── crear_producto.html   
    ├── editar_producto.html  
    └── movimientos.html      # Historial de auditoría

## Funcionalidades actuales

- Página de inicio
- Listado de productos
- Formulario para registrar nuevos productos
- Formulario para editar productos existentes
- Eliminación de productos
- Conexión con una base de datos MySQL
- Consulta de categorías asociadas a cada producto

## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python 3.x
- MySQL Server
- pip

Instala las dependencias del proyecto con:

```bash
pip install -r requirements.txt
```

> Si usas un archivo `.env`, crea uno en la raíz del proyecto con las variables de conexión necesarias.

## Configuración de la base de datos

1. Crea una base de datos MySQL.
2. Importa el archivo [database.sql](database.sql) para crear las tablas.
3. Ajusta los datos de conexión en [modulos/conexion.py](modulos/conexion.py) si tu usuario, contraseña o nombre de la base de datos son diferentes.

## Ejecución local

Desde la raíz del proyecto, ejecuta:

```bash
python app.py
```

Luego abre en tu navegador:

```text
http://localhost:5000
```

## Despliegue en producción

La aplicación está preparada para ser desplegada en Render, donde se aloja el servicio web de Flask. La base de datos MySQL se gestiona en Aiven, usando una instancia en la nube para mantener la información de forma persistente.

Para desplegarla en Render:

1. Crea un servicio web en Render apuntando al repositorio del proyecto.
2. Configura la variable de entorno necesaria para la conexión a la base de datos.
3. Asegúrate de que la instancia de MySQL en Aiven sea accesible desde Render.
4. Importa el esquema de la base de datos desde [database.sql](database.sql) en la instancia de Aiven.

## Rutas principales

- / : página inicial
- /productos : listado de productos
- /productos/crear : formulario para crear un producto
- /productos/editar/<id> : edición de un producto
- /productos/eliminar/<id> : eliminación de un producto
- /prueba_conexion : prueba de conexión con MySQL

## Estado actual del proyecto

El proyecto se encuentra en una etapa inicial, con la estructura base funcional para la gestión de productos y su conexión a una base de datos relacional.

## Próximos pasos sugeridos

- implementar autenticación de usuarios
- agregar control de movimientos de stock
- mejorar el diseño de la interfaz
- agregar validaciones más robustas en formularios
- incluir búsquedas y filtros
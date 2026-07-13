# Inventory Management System

Sistema web de gestión de inventario desarrollado con Flask, MySQL y JavaScript vanilla. Permite administrar productos, categorías y stock de forma sencilla desde una interfaz web.

## Descripción general

Este proyecto nace como una aplicación básica para controlar los productos de un negocio, mostrando información como:

- nombre del producto
- precio
- stock actual
- stock mínimo
- categoría asociada

También incluye operaciones CRUD para los productos: crear, leer, editar y eliminar.

## Tecnologías utilizadas

- Python 3
- Flask
- Jinja2
- PyMySQL
- MySQL
- HTML, CSS y JavaScript vanilla
- Render para el alojamiento de la aplicación web
- Aiven para la base de datos MySQL en la nube

## Estructura del proyecto

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
    ├── crear_producto.html
    ├── editar_producto.html
    ├── index.html
    └── productos.html
```

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
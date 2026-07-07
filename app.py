from flask import Flask, render_template, request, redirect, session, flash, jsonify
from modulos.conexion import conectar_db
from modulos.comandos_db_producto import sql_leer_productos, sql_leer_producto, sql_leer_categorias, sql_crear_producto, sql_crear_categoria, sql_actualizar_producto, sql_eliminar_producto
from modulos.comandos_db_usuario import sql_leer_usuarios, sql_leer_usuario, sql_crear_usuario, sql_actualizar_usuario, sql_eliminar_usuario, sql_verificar_usuario


app = Flask(__name__)
app.secret_key = "una_clave_secreta_y_segura_aqui"

# ---------------------------------------------------------------------------------------------
# 🛡️ GUARDIA DE SEGURIDAD (Control de Sesiones)
# ---------------------------------------------------------------------------------------------
@app.before_request
def proteger_rutas():
    rutas_publicas = ["iniciar_sesion", "test_conexion", "static"]
    # Evita que falle si se busca un archivo o ruta inexistente
    if request.endpoint and request.endpoint not in rutas_publicas and "usuario_id" not in session:
        flash("Debes iniciar sesión para acceder al sistema.", "warning")
        return redirect("/iniciar_sesion")

# ---------------------------------------------------------------------------------------------
# Prueba de conexión de DB
# ---------------------------------------------------------------------------------------------
@app.route("/prueba_conexion")
def test_conexion():
    try:
        conexion = conectar_db()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()
        conexion.close()
        return f"¡Conectado con éxito! Versión de MySQL: {version[0]}"
    except Exception as e:
        return f"Error en la conexión: {e}"

# ---------------------------------------------------------------------------------------------
# Index = Menu principal
# ---------------------------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------------------------------------------------------------------------
# Login, administración de usuarios y registro de estos
# ---------------------------------------------------------------------------------------------

@app.route("/iniciar_sesion", methods=["GET", "POST"])
def iniciar_sesion():
    if request.method == "POST":
        nombre_usuario = request.form["nombre_usuario"]
        contraseña_usuario = request.form["contraseña_usuario"]
        usuario_valido = sql_verificar_usuario(nombre_usuario, contraseña_usuario)
        
        if usuario_valido:
            # Si los datos son correctos, guardamos al usuario en la sesión
            session["usuario_id"] = usuario_valido["idusuarios"]
            session["name"] = usuario_valido["nombre"] 
            session["rol"] = usuario_valido["rol"]
            return redirect("/")
        
        else:
        # Si devuelve None, guardamos el mensaje de error "en el aire"
            flash("Usuario o contraseña incorrectos. Por favor, intenta de nuevo.", "error")    
    
    return render_template("iniciar_sesion.html")

@app.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear() # Borra todo lo que haya en la sesión (id, nombre, rol)
    flash("Sesión cerrada correctamente.", "success")
    return redirect("/iniciar_sesion")

@app.route("/usuarios")
def listado_usuarios():
    lista_usuarios = sql_leer_usuarios()
    
    return render_template("usuarios.html", usuarios = lista_usuarios)

@app.route("/usuarios/crear", methods=["GET", "POST"])
def registrar_usuarios():
    """Recibe la informacion enviada por el formulario"""
    if request.method == "POST":
        nombre_usuario = request.form["nombre_usuario"]
        mail_usuario = request.form["mail_usuario"]
        contraseña_usuario = request.form["contraseña_usuario"]
        rol_usuario = request.form["rol_usuario"]
        
        sql_crear_usuario(nombre_usuario, contraseña_usuario, mail_usuario, rol_usuario)
        return redirect("/usuarios")
    
    
    return render_template("crear_usuario.html")

@app.route("/usuario/editar/<int:id>", methods=["GET","POST"])
def editar_usuario(id):
    if request.method == "POST":
        """Recibo los valores enviados por el formulario"""
        nombre_usuario = request.form["nombre_usuario"]
        mail_usuario = request.form["mail_usuario"]
        contraseña = request.form["contraseña_usuario"]
        rol_usuario = request.form["rol_usuario"]
        
        nueva_contraseña = contraseña if contraseña.strip() != "" else None
        contraseña_usuario = nueva_contraseña
        
        """Ahora voy a actualizar los datos"""
        if sql_actualizar_usuario(nombre_usuario, contraseña_usuario, mail_usuario, rol_usuario, id) == True:
            return redirect("/usuarios")
        else:
            flash("Error al actualizar el usuario", "error")
        
    usuario_devuelto = sql_leer_usuario(id)
    
    return render_template("editar_usuario.html", usuario = usuario_devuelto) 

@app.route("/usuarios/eliminar/<int:id>")
def eliminar_usuario(id):
    sql_eliminar_usuario(id)
    return redirect("/usuarios")

# ---------------------------------------------------------------------------------------------
# PRODUCTOS
# ---------------------------------------------------------------------------------------------
@app.route("/productos")
def listado_productos():
    
    lista_productos = sql_leer_productos()
    
    return render_template("productos.html", productos = lista_productos)

@app.route("/productos/crear", methods=["GET", "POST"])
def registrar_producto():
    """Recibe la informacion enviada por el formulario"""
    if request.method == "POST":
        nombre_producto = request.form["nombre_producto"]
        precio_producto = request.form["precio_producto"]
        stok_actual_producto = request.form["stok_actual_producto"]
        stok_minimo_producto = request.form["stok_minimo_producto"]
        categoria_producto = request.form["idcategorias"]
        
        sql_crear_producto(nombre_producto, precio_producto, stok_actual_producto, stok_minimo_producto, categoria_producto)
        return redirect("/productos")
    
    """Carga el formulario y las opciones de categorias"""
    lista_categorias = sql_leer_categorias()
    
    return render_template("crear_producto.html", categorias= lista_categorias)

@app.route("/productos/crear/categoria", methods=["GET", "POST"])
def registrar_categoria():
    if request.method == "POST":
        nombre_categoria = request.form["nombre_categoria"]
        
        sql_crear_categoria(nombre_categoria)
        return redirect("/productos")
    
    return render_template("crear_categoria.html")

@app.route("/productos/editar/<int:id>", methods=["GET","POST"])
def editar_producto(id):
    if request.method == "POST":
        """Recibo los valores enviados por el formulario"""
        nombre_producto = request.form["nombre_producto"]
        precio_producto = request.form["precio_producto"]
        stok_actual_producto = request.form["stok_actual_producto"]
        stok_minimo_producto = request.form["stok_minimo_producto"]
        categoria_producto = request.form["idcategorias"]
        
        """Ahora voy a actualizar los datos"""
        if sql_actualizar_producto(nombre_producto, precio_producto, stok_actual_producto, stok_minimo_producto, categoria_producto, id) == True:
            return redirect("/productos")
        else:
            flash("Error al actualizar el producto", "error")
        
    producto_devuelto = sql_leer_producto(id)
    lista_categorias = sql_leer_categorias()
    
    return render_template("editar_producto.html", producto = producto_devuelto, categorias = lista_categorias) 

@app.route("/productos/eliminar/<int:id>")
def eliminar_producto(id):
    sql_eliminar_producto(id)
    return redirect("/productos")


if __name__ == "__main__":
    app.run(debug=True)
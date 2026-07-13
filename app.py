from flask import Flask, render_template, request, redirect, session, flash, jsonify
from modulos.comandos_db_producto import sql_leer_productos, sql_leer_producto, sql_leer_categorias, sql_crear_producto, sql_crear_categoria, sql_actualizar_producto, sql_eliminar_producto, sql_aumentar_cantidad, sql_decrementar_cantidad
from modulos.comandos_db_usuario import sql_leer_usuarios, sql_leer_usuario, sql_crear_usuario, sql_actualizar_usuario, sql_eliminar_usuario, sql_verificar_usuario
from modulos.comandos_db_alerta import sql_alertar_stock, test_conexion
from modulos.comandos_db_movimientos import sql_leer_movimientos, sql_crear_movimientos

app = Flask(__name__)
app.secret_key = "una_clave_secreta_y_segura_aqui"



# ---------------------------------------------------------------------------------------------
# 🛡️ GUARDIA DE SEGURIDAD (Control de Sesiones y Roles)
# ---------------------------------------------------------------------------------------------
@app.before_request
def proteger_rutas():
    rutas_publicas = ["iniciar_sesion", "static"]
    
    # Ruta no existe o es pública
    if not request.endpoint or request.endpoint in rutas_publicas:
        return
        
    # Control de autenticación general
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para acceder al sistema", "warning")
        return redirect("/iniciar_sesion")
        
    # Mapeo de accesos utilizando el NOMBRE DE LAS FUNCIONES
    permisos_roles = {
        "admin": [
            "index", 
            "listado_usuarios", "registrar_usuarios", "editar_usuario", "eliminar_usuario",
            "listado_productos", "registrar_producto", "registrar_categoria", "editar_producto", 
            "aumentar_cantidad", "decrementar_cantidad", "eliminar_producto",
            "listado_historial"
        ],
        "operario": [
            "index",  # El operario necesita ver la raíz para usar el menú
            "listado_productos", "registrar_producto", "registrar_categoria", "editar_producto", 
            "aumentar_cantidad", "decrementar_cantidad", "eliminar_producto"
        ]
    }
    
    rol_usuario = session.get("rol")
    ruta_actual = request.endpoint  # Contiene el nombre de la función (ej: "listado_usuarios")
    
    # Verificamos si la función actual está contemplada en nuestro sistema de permisos
    ruta_protegida = any(ruta_actual in rutas for rutas in permisos_roles.values())
    
    if ruta_protegida:
        rutas_permitidas = permisos_roles.get(rol_usuario, [])
        
        # Si el rol del usuario no tiene esta función en su lista, lo rebotamos
        if ruta_actual not in rutas_permitidas:
            flash("No tienes permisos suficientes para acceder a esta sección.", "warning")
            return redirect("/")
        

# ---------------------------------------------------------------------------------------------
# Index = Menu principal
# ---------------------------------------------------------------------------------------------
@app.route("/")
def index():
    listado_productos_bajos = sql_alertar_stock()
    if listado_productos_bajos:
        flash("Productos bajos en stock", "warning" )

    
    if not test_conexion:
        return flash("Error al conectar con la base de datos", "warning")    
    
    return render_template("index.html", productos_bajos = listado_productos_bajos)

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
    
    listado_productos_bajos = sql_alertar_stock()
    if listado_productos_bajos:
        flash("Productos bajos en stock", "warning" )
    
    if not test_conexion:
        return flash("Error al conectar con la base de datos", "warning")    
    
    return render_template("usuarios.html", usuarios = lista_usuarios, productos_bajos = listado_productos_bajos)

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
    
    listado_productos_bajos = sql_alertar_stock()
    if listado_productos_bajos:
        flash("Productos bajos en stock", "warning" )
    
    if not test_conexion:
        return flash("Error al conectar con la base de datos", "warning")    
    
    return render_template("productos.html", productos = lista_productos, productos_bajos = listado_productos_bajos)

@app.route("/productos/crear", methods=["GET", "POST"])
def registrar_producto():
    """Recibe la informacion enviada por el formulario"""
    if request.method == "POST":
        nombre_producto = request.form["nombre_producto"]
        precio_producto = float(request.form.get("precio_producto", 0) or 0)
        stok_actual_producto = int(request.form.get("stok_actual_producto", 0) or 0)
        stok_minimo_producto = int(request.form.get("stok_minimo_producto", 0) or 0)
        categoria_producto = int(request.form["idcategorias"])
        
        id_nuevo_producto = sql_crear_producto(nombre_producto, precio_producto, stok_actual_producto, stok_minimo_producto, categoria_producto)
        id_usuario = session["usuario_id"]
        sql_crear_movimientos(id_nuevo_producto, id_usuario, "ALTA", cantidad=stok_actual_producto)
        
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
        stok_minimo_producto = request.form["stok_minimo_producto"]
        categoria_producto = request.form["idcategorias"]
        
        """Ahora voy a actualizar los datos"""
        if sql_actualizar_producto(nombre_producto, precio_producto, stok_minimo_producto, categoria_producto, id) == True:
            id_producto = id
            id_usuario = session["usuario_id"]
            sql_crear_movimientos(id_producto, id_usuario, "MODIFICACIÓN", cantidad=None)
            return redirect("/productos")
        else:
            flash("Error al actualizar el producto", "error")
        
    producto_devuelto = sql_leer_producto(id)
    lista_categorias = sql_leer_categorias()
    
    return render_template("editar_producto.html", producto = producto_devuelto, categorias = lista_categorias) 

@app.route("/productos/aumentar/<int:id>", methods=["GET", "POST"])
def aumentar_cantidad(id):
    if "usuario_id" not in session:
        return jsonify({"status": "error", "message": "Sesión expirada"}), 401
    
    
    
    if request.method == "POST":
        try:
            cantidad_a_sumar = int(request.form.get("nuevo_stock",0))
            
            if cantidad_a_sumar <= 0:
                return jsonify({"status": "error", "message": "La cantidad debe ser mayor a cero"}), 400
        
            if sql_aumentar_cantidad(id, cantidad_a_sumar):
                id_usuario = session["usuario_id"]
                sql_crear_movimientos(id, id_usuario, "INGRESO", cantidad=cantidad_a_sumar)
            
                producto_actualizado = sql_leer_producto(id)
                nuevo_stock_total = producto_actualizado["stock_actual"]
                
                return jsonify({
                    "status": "success",
                    "messege": "Stock incrementado correctamente",
                    "nuevo_stock": nuevo_stock_total
                })
            else:
                return jsonify({"status": "error", "message": "No se pudo actualizar en la base de datos"}), 500
        except Exception as e:
            print("Error en API aumentar stock:", e)
            return jsonify({"status": "error", "message": "Error interno del servidor"}), 500
    
    producto_devuelto = sql_leer_producto(id)
    return render_template("aumentar_producto.html", producto = producto_devuelto)
    

    
@app.route("/productos/decrementar/<int:id>", methods=["GET", "POST"])
def decrementar_cantidad(id):
    
    producto_devuelto = sql_leer_producto(id)
    
    if request.form == "POST":
        cantidad_a_restar = int(request.form["nuevo_stock"])
        
        if cantidad_a_restar > producto_devuelto["stock_actual"]:
            flash(f"Error: No puedes retirar {cantidad_a_restar} unidades. El stock actual es de {producto_devuelto['stock_actual']}.", "error")
            return render_template("decrementar_cantidad.html", producto = producto_devuelto)
        
        elif cantidad_a_restar <= 0:
            flash("Error: La cantidad a retirar debe ser mayor a cero.", "error")
            return render_template("decrementar_cantidad.html", producto = producto_devuelto)
    
        if sql_decrementar_cantidad(id, cantidad_a_restar):
            id_producto = id
            id_usuario = session["usuario_id"]
            sql_crear_movimientos(id_producto, id_usuario, "EGRESO", cantidad=cantidad_a_restar)
            return redirect("/productos")
        else:
            flash("Error al actualizar el producto", "error")
    
    
    return render_template("decrementar_cantidad.html", producto = producto_devuelto)


@app.route("/productos/eliminar/<int:id>")
def eliminar_producto(id):
    sql_eliminar_producto(id)
    id_producto = id
    id_usuario = session["usuario_id"]
    sql_crear_movimientos(id_producto, id_usuario, "BAJA", cantidad=None)
    
    return redirect("/productos")

# ---------------------------------------------------------------------------------------------
# Historial de movimientos
# ---------------------------------------------------------------------------------------------
@app.route("/historial_movimiento")
def listado_historial():
    
    if not test_conexion:
        return flash("Error al conectar con la base de datos", "warning")    

    listado_historial = sql_leer_movimientos()
    return render_template("historial_movimiento.html", movimientos = listado_historial)


if __name__ == "__main__":
    app.run(debug=True)
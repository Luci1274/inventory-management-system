from flask import Flask, render_template, request, redirect
from modulos.conexion import conectar_db
from modulos.comandos_db_producto import sql_leer_productos, sql_leer_producto, sql_leer_categorias, sql_crear_producto, sql_actualizar_producto, sql_eliminar_producto
app = Flask(__name__)


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
    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/productos")
def productos():
    
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
            error = "Hubo un error al guardar los datos"
            return error, 500
        
    producto = sql_leer_producto(id)
    lista_categorias = sql_leer_categorias()
    
    return render_template("editar_producto.html", producto = producto, categorias = lista_categorias) 

@app.route("/productos/eliminar/<int:id>")
def eliminar_producto(id):
    sql_eliminar_producto(id)
    return redirect("/productos")


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
from modulos.conexion import conectar_db
from modulos.registrar_producto import crear_producto
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
    render_template("index.html")

@app.route("/productos")
def productos():
    return render_template("productos.html")

@app.route("/productos/crear", methods=["GET", "POST"])
def registrar_producto():
    if request.method == "POST":
        nombre_producto = request.form["nombre_producto"]
        precio_producto = request.form["precio_producto"]
        stok_actual_producto = request.form["stok_actual_producto"]
        stok_minimo_producto = request.form["stok_minimo_producto"]
        categoria_producto = request.form["idcategorias"]
        
        crear_producto(nombre_producto, precio_producto, stok_actual_producto, stok_minimo_producto, categoria_producto)
        return redirect("/productos")
    
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM categorias;")
    lista_categorias = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template("crear.html", categorias= lista_categorias)

@app.route("/productos/editar/<int:id>", methods=["GET","POST"])
def editar_producto():
    return render_template("editar.html") 
    
if __name__ == "__main__":
    app.run(debug=True)
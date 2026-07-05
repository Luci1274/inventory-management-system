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
    
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT p.idproductos, p.nombre, p.precio, p.stock_actual, c.nombre AS categoria FROM productos AS p JOIN categorias AS c ON  p.idcategorias = c.idcategorias;")
    lista_productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template("productos.html", productos = lista_productos)

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
    """Busca todas las categorias de los productos"""
    cursor.execute("SELECT * FROM categorias;")
    lista_categorias = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template("crear_producto.html", categorias= lista_categorias)

@app.route("/productos/editar/<int:id>", methods=["GET","POST"])
def editar_producto(id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    if request.method == "POST":
        """Recibo los valores enviados por el formulario"""
        nombre_producto = request.form["nombre_producto"]
        precio_producto = request.form["precio_producto"]
        stok_actual_producto = request.form["stok_actual_producto"]
        stok_minimo_producto = request.form["stok_minimo_producto"]
        categoria_producto = request.form["idcategorias"]
        
        """Ahora voy a actualizar los datos"""
        try:
            cursor.execute("UPDATE productos SET nombre = %s, precio = %s, stock_actual = %s, stock_minimo = %s, idcategoria = %s WHERE idproductos = %s;", (nombre_producto, precio_producto, stok_actual_producto, stok_minimo_producto, categoria_producto, id))
            conexion.commit()
            return redirect("/productos")
        except Exception as e:
            """En el caso de haber un error deshace los cambios"""
            conexion.rollback()
        cursor.close()
        conexion.close()
        return "Hubo un error al guardar los datos", 500
        
    """Busca la informacion del producto correspondiente"""
    cursor.execute("SELECT p.idproductos, p.nombre, p.precio, p.stock_actual, p.stock_minimo, c.nombre AS categoria FROM productos AS p WHERE p.idproductos = %s;", (id,))
    producto = cursor.fetchone()
    cursor.execute("SELECT * FROM categorias;")
    lista_categorias = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("editar_producto.html", producto = producto, categorias = lista_categorias) 

@app.route("/productos/eliminar/<int:id>")
def eliminar_producto(id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    """Intenta borrar el producto seleccionado"""
    try:    
        cursor.execute("DELETE FROM productos WHERE idproductos = %s;", (id,))
        conexion.commit()
    except Exception as e:
        """En el caso de haber un error deshace los cambios"""
        conexion.rollback()
    cursor.close()
    conexion.close()
    return redirect("/productos")


if __name__ == "__main__":
    app.run(debug=True)
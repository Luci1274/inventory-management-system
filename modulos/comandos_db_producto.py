from modulos.conexion import conectar_db
#-------------------------------------------------------------------
def sql_leer_productos():
    """Lee la tabla de productos y devuele el listado"""
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT p.idproductos, p.nombre, p.precio, p.stock_actual, c.nombre AS categoria FROM productos AS p JOIN categorias AS c ON  p.idcategorias = c.idcategorias WHERE activo = 1;")
    lista_productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return lista_productos
#-------------------------------------------------------------------
def sql_leer_producto(id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    """Busca la informacion del producto correspondiente"""
    cursor.execute("SELECT idproductos, nombre, precio, stock_actual, stock_minimo, idcategorias FROM productos WHERE idproductos = %s;", (id,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return producto
#-------------------------------------------------------------------
def sql_leer_categorias():
    """Lee la tabla de cateogias y devuelve el listado"""
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    """Busca todas las categorias de los productos"""
    cursor.execute("SELECT * FROM categorias;")
    lista_categorias = cursor.fetchall()
    cursor.close()
    conexion.close()
    return lista_categorias
#-------------------------------------------------------------------
def sql_crear_producto(nombre_producto, precio_producto, stok_actual_producto, stok_minimo_producto, categoria_producto):
    """Registra un nuevo producto"""
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    sql = "INSERT INTO productos (nombre, precio, stock_actual, stock_minimo, idcategorias) VALUES (%s, %s, %s, %s, %s)"
    valores = (nombre_producto, precio_producto, stok_actual_producto, stok_minimo_producto, categoria_producto)
    cursor.execute(sql, valores)
    conexion.commit()
    id_nuevo_producto = cursor.lastrowid()
    cursor.close()
    conexion.close()
    return id_nuevo_producto
#------------------------------------------------------------------- 
def sql_crear_categoria(categoria):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    sql = "INSERT INTO categorias (nombre) VALUES (%s)"
    valor = (categoria,)
    cursor.execute(sql, valor)
    conexion.commit()
    
    cursor.close()
    conexion.close()
#-------------------------------------------------------------------   
def sql_actualizar_producto(nombre_producto, precio_producto, stok_actual_producto, stok_minimo_producto, categoria_producto, id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("UPDATE productos SET nombre = %s, precio = %s, stock_actual = %s, stock_minimo = %s, idcategorias = %s WHERE idproductos = %s;", (nombre_producto, precio_producto, stok_actual_producto, stok_minimo_producto, categoria_producto, id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        """En el caso de haber un error deshace los cambios"""
        conexion.rollback()
        cursor.close()
        conexion.close()
        print("❌ ERROR EN UPDATE:", e)
        return False
#-------------------------------------------------------------------
def sql_eliminar_producto(id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    """Intenta borrar el producto seleccionado"""
    try:    
        cursor.execute("UPADATE productos SET activo = 0 WHERE idproductos = %s;", (id,))
        conexion.commit()
    except Exception as e:
        """En el caso de haber un error deshace los cambios"""
        conexion.rollback()
    cursor.close()
    conexion.close()
#-------------------------------------------------------------------
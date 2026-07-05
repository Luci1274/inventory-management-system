from modulos.conexion import conectar_db

def crear_producto(nombre_producto, precio_producto, stok_actual_producto, stok_minimo_producto, categoria_producto):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    sql = "INSERT INTO productos (nombre, precio, stock_actual, stock_minimo, idcategorias) VALUES (%s, %s, %s, %s, %s)"
    valores = (nombre_producto, precio_producto, stok_actual_producto, stok_minimo_producto, categoria_producto)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()
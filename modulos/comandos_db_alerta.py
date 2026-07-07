from modulos.conexion import conectar_db

#-------------------------------------------------------------------
def sql_alertar_stock():
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT p.nombre, p.stock_actual, c.nombre AS categoria FROM productos AS p JOIN categorias AS c ON  p.idcategorias = c.idcategorias WHERE stock_actual <= stock_minimo;")
    
    lista_productos_bajos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return lista_productos_bajos
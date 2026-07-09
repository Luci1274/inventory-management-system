from modulos.conexion import conectar_db

#-------------------------------------------------------------------
def sql_leer_movimientos():
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT p.nombre AS nombre_producto, u.nombre AS usuarios, m.cantidad, m.tipo_movimiento AS movimiento, m.fecha_hora FROM usuarios AS u JOIN movimientos_stock AS m ON u.idusuarios = m.idusuarios JOIN productos AS p ON m.idproductos = p.idproductos;")
    
    lista_movimientos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return lista_movimientos

#-------------------------------------------------------------------
def sql_crear_movimientos(id_producto, id_usuario, tipo_movimiento, cantidad=None):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    sql = ("INSERT INTO movimientos_stock (idproductos, idusuarios, cantidad, tipo_movimiento, fecha_hora) VALUES (%s,%s,%s,%s,NOW());")
    valores = (id_producto, id_usuario, cantidad, tipo_movimiento)
    cursor.execute(sql, valores)
    conexion.commit()
    
    cursor.close()
    conexion.close()

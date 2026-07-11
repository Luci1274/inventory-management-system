from werkzeug.security import check_password_hash, generate_password_hash 
from modulos.conexion import conectar_db

#-------------------------------------------------------------------
def sql_leer_usuarios():
    """Lee la tabla de usuarios y devuele el listado"""
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT idusuarios, nombre,  email, rol FROM usuarios WHERE activo = 1;")
    lista_usuarios = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    return lista_usuarios
#-------------------------------------------------------------------
def sql_leer_usuario(id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    """Busca la informacion del usuario correspondiente"""
    cursor.execute("SELECT idusuarios, nombre, email, rol FROM usuarios WHERE idusuarios = %s;", (id,))
    usuario = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    return usuario
#-------------------------------------------------------------------
def sql_crear_usuario(nombre_usuario, contraseña_usuario, mail_usuario, rol_usuario):
    """Registra un nuevo usuario"""
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    """Hasear contraseña"""
    contraseña_haseada = generate_password_hash(contraseña_usuario)
    
    sql = "INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s);"
    valores = (nombre_usuario, mail_usuario, contraseña_haseada, rol_usuario)
    cursor.execute(sql, valores)
    conexion.commit()
    
    cursor.close()
    conexion.close()
#-------------------------------------------------------------------
def sql_actualizar_usuario(nombre_usuario, contraseña_usuario, mail_usuario, rol_usuario, id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    try:
        if contraseña_usuario:
            contraseña_haseada = generate_password_hash(contraseña_usuario)    
            sql = "UPDATE usuarios SET nombre = %s, email = %s, password = %s, rol = %s WHERE idusuarios = %s;"
            valores = (nombre_usuario, mail_usuario, contraseña_haseada, rol_usuario, id)
        
        else:
            # Si vino vacío, actualizamos todo MENOS la columna password (la dejamos intacta)
            sql = "UPDATE usuarios SET nombre = %s, email = %s, rol = %s WHERE idusuarios = %s;"
            valores = (nombre_usuario, mail_usuario, rol_usuario, id)
        
        cursor.execute(sql,valores)
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
def sql_eliminar_usuario(id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    """Intenta borrar el usuario seleccionado"""
    try:    
        cursor.execute("UPDATE usuarios SET activo = 0 WHERE idusuarios = %s;", (id,))
        conexion.commit()
    except Exception as e:
        """En el caso de haber un error deshace los cambios"""
        conexion.rollback()
    cursor.close()
    conexion.close()
#-------------------------------------------------------------------
def sql_verificar_usuario(nombre_ingresado, password_ingresada):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # 1. Buscamos al usuario únicamente por su nombre
    cursor.execute("SELECT idusuarios, nombre, password, rol FROM usuarios WHERE nombre = %s;", (nombre_ingresado,))
    usuario = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    
    # 2. Si el usuario existe, usamos la función mágica de Flask para comparar los hashes
    if usuario:
        # check_password_hash recibe (el hash guardado, la clave en texto plano del formulario)
        if check_password_hash(usuario['password'], password_ingresada):
            return usuario # ¡Contraseña correcta! Retornamos los datos del usuario
            
    return None # Si no existe o la contraseña no coincide
#-------------------------------------------------------------------

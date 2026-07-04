import pymysql

#configuración de la conexión
def conectar_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1274",
        database="gestion_stock",
        cursorclass=pymysql.cursors.DictCursor
    )

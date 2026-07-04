from flask import Flask
from modulos.conexion import conectar_db
app = Flask(__name__)


@app.route("/")
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
    
if __name__ == "__main__":
    app.run(debug=True)
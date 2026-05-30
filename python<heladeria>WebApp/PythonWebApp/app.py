from flask import Flask, render_template, request, redirect
import mysql.connector
from config import Config

# Se crea la instancia de la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Función para obtener conexión directamente
def get_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

# Ruta página inicio
@app.route('/')
def inicio():
    return render_template('index.html')

# Ruta página categorias, muestra todas las categorias.
@app.route('/categorias')
def categorias():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_categoria, nombre, descripcion FROM categorias")
    categorias = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('categorias.html', categorias=categorias)

# Iniciar servidor de desarrollo
if __name__ == "__main__":
    app.run(debug=True)
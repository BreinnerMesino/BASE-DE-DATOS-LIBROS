from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Configuración de la conexión a la base de datos
conn = pyodbc.connect(
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\brein\Desktop\CODIGO BPDS\BaseDeDatosLibros\myprojectweb\libros.accdb;"
)
cursor = conn.cursor()

# Rutas
@app.route('/')
def index():
    # Obtener libros de la base de datos
    cursor.execute('SELECT * FROM libros')
    libros = cursor.fetchall()
    return render_template('index.html', libros=libros)

@app.route('/agregar_libro', methods=['POST'])
def agregar_libro():
    if request.method == 'POST':
        nombre_libro = request.form['nombre_libro']
        nombre_autor = request.form['nombre_autor']
        estado = request.form['estado']

        # Insertar libro en la base de datos
        cursor.execute(
            'INSERT INTO libros (nombre_libro, nombre_autor, estado) VALUES (?, ?, ?)',
            nombre_libro, nombre_autor, estado
        )
        conn.commit()

    return redirect(url_for('index'))
# ...

@app.route('/eliminar_libro/<int:libro_id>', methods=['POST'])
def eliminar_libro(libro_id):
    if request.method == 'POST':
        # Eliminar libro de la base de datos
        cursor.execute('DELETE FROM libros WHERE id = ?', libro_id)
        conn.commit()

        return redirect(url_for('index'))

# ...


# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)

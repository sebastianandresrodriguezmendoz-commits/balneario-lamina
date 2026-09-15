from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Función para conectarse a MySQL en XAMPP
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='bhnjcfoau3pkxfla4ld2-mysql.services.clever-cloud.com',
        database='bhnjcfoau3pkxfla4ld2',
        user='u9cam7rcdvbwqsct',
        password='x89eBUAywX4u4fN5R2Qv',  
        port=3306
    )

# Ruta principal que muestra el sitio web
@app.route('/')
def inicio():
    return render_template('mina.html')

# Ruta que recibe los datos del formulario y los guarda en MySQL
@app.route('/guardar_contacto', methods=['POST'])
def guardar_contacto():
    datos = request.get_json()
    
    nombre = datos.get('nombre')
    email = datos.get('email')
    telefono = datos.get('telefono')
    mensaje = datos.get('mensaje')

    if not nombre or not email or not mensaje:
        return jsonify({'status': 'error', 'mensaje': 'Por favor llena todos los campos obligatorios.'}), 400

    try:
        conexion = obtener_conexion_bd()
        cursor = conexion.cursor()
        
        sql = "INSERT INTO contactos (nombre, email, telefono, mensaje) VALUES (%s, %s, %s, %s)"
        valores = (nombre, email, telefono, mensaje)
        
        cursor.execute(sql, valores)
        conexion.commit()
        
        cursor.close()
        conexion.close()
        
        return jsonify({'status': 'ok', 'mensaje': '¡Gracias por contactarnos! Tu mensaje fue guardado exitosamente.'}), 200

    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'mensaje': f'Error en la base de datos: {err}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
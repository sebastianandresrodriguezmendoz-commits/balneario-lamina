from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='bhnjcfoau3pkxfla4ld2-mysql.services.clever-cloud.com',
        database='bhnjcfoau3pkxfla4ld2',
        user='u9cam7rcdvbwqsct',
        password='x89eBUAywX4u4fN5R2Qv',  
        port=3306
    )

@app.route('/')
def inicio():
    return render_template('mina.html')

# --- RUTAS DE CONTACTO ---

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
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        sql = "INSERT INTO contactos (nombre, correo, telefono, mensaje) VALUES (%s, %s, %s, %s)"
        valores = (nombre, email, telefono, mensaje)
        
        cursor.execute(sql, valores)
        conexion.commit()
        
        cursor.close()
        conexion.close()
        
        return jsonify({'status': 'ok', 'mensaje': '¡Gracias por contactarnos! Tu mensaje fue guardado exitosamente.'}), 200

    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'mensaje': f'Error en la base de datos: {err}'}), 500

@app.route('/admin')
def admin_contactos():
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id, nombre, correo, telefono, mensaje, fecha FROM contactos ORDER BY id DESC")
        contactos = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        
        return render_template('admin.html', contactos=contactos)
    except mysql.connector.Error as err:
        return f"Error al consultar la base de datos: {err}", 500

# --- NUEVAS RUTAS DE SUGERENCIAS / POSTS ---

@app.route('/guardar_sugerencia', methods=['POST'])
def guardar_sugerencia():
    datos = request.get_json()
    
    nombre = datos.get('nombre')
    calificacion = datos.get('calificacion')
    sugerencia = datos.get('sugerencia')

    if not calificacion or not sugerencia:
        return jsonify({'status': 'error', 'mensaje': 'Por favor completa la calificación y tu sugerencia.'}), 400

    # Asigna 'Visitante' si el usuario no ingresó su nombre
    nombre_final = nombre.strip() if nombre and nombre.strip() else 'Visitante'

    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        sql = "INSERT INTO sugerencias (nombre, calificacion, sugerencia) VALUES (%s, %s, %s)"
        valores = (nombre_final, int(calificacion), sugerencia)
        
        cursor.execute(sql, valores)
        conexion.commit()
        
        cursor.close()
        conexion.close()
        
        return jsonify({'status': 'ok', 'mensaje': '¡Gracias! Tu opinión ha sido publicada exitosamente.'}), 200

    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'mensaje': f'Error en la base de datos: {err}'}), 500

@app.route('/obtener_sugerencias', methods=['GET'])
def obtener_sugerencias():
    try:
        conexion = get_db_connection()
        # Usamos dictionary=True para que Flask pueda convertir los datos a JSON fácilmente
        cursor = conexion.cursor(dictionary=True)
        
        cursor.execute("SELECT id, nombre, calificacion, sugerencia, DATE_FORMAT(fecha, '%d/%m/%Y') AS fecha FROM sugerencias ORDER BY id DESC")
        sugerencias = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        
        return jsonify(sugerencias), 200

    except mysql.connector.Error as err:
        return jsonify([]), 500

if __name__ == '__main__':
    app.run(debug=True)
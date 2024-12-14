# Copyright © 2024 Daniel Alzate (xStevenx). Todos los derechos reservados.
# Este software está protegido bajo las leyes de derechos de autor.
import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',  # Usuario por defecto de XAMPP
    'password': '',  # Deja esto vacío si no configuraste una contraseña
    'database': 'empleados'  # Nombre de tu base de datos
}

# Función para insertar datos en la base de datos
# Función para insertar datos en la base de datos
def guardar_datos_en_db(cedula, nombre, apellido, telefono, horas, valor_hora, salario):
    connection = None  # Inicializa la variable
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = """
        INSERT INTO empleados (cedula, nombre, apellido, telefono, horas, valor_hora, salario)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (cedula, nombre, apellido, telefono, horas, valor_hora, salario))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Función para calcular el salario
def calcular_salario(horas, valor_hora):
    if horas <= 40:
        return horas * valor_hora
    elif horas <= 48:
        salario_normal = 40 * valor_hora
        horas_extra = horas - 40
        salario_extra = horas_extra * valor_hora * 1.2
        return salario_normal + salario_extra
    else:
        salario_normal = 40 * valor_hora
        salario_extra_simple = 8 * valor_hora * 1.2
        horas_extra_doble = horas - 48
        salario_extra_doble = horas_extra_doble * valor_hora * 1.4
        return salario_normal + salario_extra_simple + salario_extra_doble

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    cedula = request.form['cedula']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    horas = int(request.form['horas'])
    valor_hora = float(request.form['valor_hora'])
    
    salario = calcular_salario(horas, valor_hora)
    guardar_datos_en_db(cedula, nombre, apellido, telefono, horas, valor_hora, salario)
    
    return render_template(
        'resultado.html',
        cedula=cedula,
        nombre=nombre,
        apellido=apellido,
        telefono=telefono,
        salario=salario
    )

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos de ejemplo en memoria
usuarios = [
    {
        'id_User': 1,
        'nombre': 'jase',
        'correo': 'jase@gmail.com',
        'password': 'jose123',
     },
]

autos = [
    {
        'patente': 'HSD451056',
        'id_User': 1, 
        'marca': 'ONDA',
        'modelo': '2015',
    
    },
]

reemplazos = [
    {
        'id_replace': 1,
        'id_User': 1,
        'patente': 'HSD451056',
        'descripcion': 'Reemplazo1',
        'tiempo_inicio': "2022-02-22",
        'desde': "2022-02-22",
        'hasta': "2022-02-22",
        'partCar': "motor",
    },
]


# obtener un usuario por su ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def obtener_usuario(user_id):
    usuario = next((user for user in usuarios if user['id_User'] == user_id), None)
    if usuario:
        return jsonify({'usuario': usuario})
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

# agregar un nuevo usuario
@app.route('/api/users', methods=['POST'])
def agregar_usuario():
    campos_necesarios = ['nombre', 'correo', 'password']
    if not all(campo in request.json for campo in campos_necesarios):
        return jsonify({'error': f'Se requieren los campos {", ".join(campos_necesarios)} para agregar un usuario'}), 400

    # Verificar correo ya esta en uso
    if any(user['correo'] == request.json['correo'] for user in usuarios):
        return jsonify({'error': 'El correo ya está en uso'}), 400

    nuevo_usuario = {
        'id_User': len(usuarios) + 1,
        'nombre': request.json['nombre'],
        'correo': request.json['correo'],
        'password': request.json['password']
    }
    usuarios.append(nuevo_usuario)
    return jsonify({'mensaje': 'Usuario agregado correctamente', 'usuario': nuevo_usuario}), 201


# obtener un auto por su patente
@app.route('/api/cars/<string:patente>', methods=['GET'])
def obtener_auto(patente):
    auto = next((car for car in autos if car['patente'] == patente), None)
    if auto:
        return jsonify({'auto': auto})
    else:
        return jsonify({'error': 'Auto no encontrado'}), 404

#  agregar un nuevo auto
@app.route('/api/cars', methods=['POST'])
def agregar_auto():
    campos_necesarios = ['patente', 'marca', 'modelo', 'id_User']
    if not all(campo in request.json for campo in campos_necesarios):
        return jsonify({'error': f'Se requieren los campos {", ".join(campos_necesarios)} para agregar un auto'}), 400

    # Verificar si el usuario existe antes de agregar el auto
    usuario_existente = next((user for user in usuarios if user['id_User'] == request.json['id_User']), None)
    if not usuario_existente:
        return jsonify({'error': 'El usuario especificado no existe'}), 400

    nuevo_auto = {
        'patente': request.json['patente'],
        'marca': request.json['marca'],
        'modelo': request.json['modelo'],
        'id_User': request.json['id_User']
    }
    autos.append(nuevo_auto)
    return jsonify({'mensaje': 'Auto agregado correctamente', 'auto': nuevo_auto}), 201

#  obtener todos los reemplazos de un auto por patente
@app.route('/api/replaces/por-patente/<string:patente>', methods=['GET'])
def obtener_reemplazos_por_patente(patente):
    reemplazos_por_patente = [replace for replace in reemplazos if replace['patente'] == patente]
    if reemplazos_por_patente:
        return jsonify({'reemplazos': reemplazos_por_patente})
    else:
        return jsonify({'error': 'No se encontraron reemplazos para la patente especificada'}), 404


# obtener un reemplazo por su ID
@app.route('/api/replaces/<int:replace_id>', methods=['GET'])
def obtener_reemplazo(replace_id):
    reemplazo = next((replace for replace in reemplazos if replace['id_replace'] == replace_id), None)
    if reemplazo:
        return jsonify({'reemplazo': reemplazo})
    else:
        return jsonify({'error': 'Reemplazo no encontrado'}), 404

#  agregar un nuevo reemplazo
@app.route('/api/replaces', methods=['POST'])
def agregar_reemplazo():
    campos_necesarios = ['id_User', 'patente', 'descripcion', 'tiempo_inicio', 'desde', 'hasta', 'partCar']
    if not all(campo in request.json for campo in campos_necesarios):
        return jsonify({'error': f'Se requieren los campos {", ".join(campos_necesarios)} para agregar un reemplazo'}), 400

    # Verificar si el usuario existe antes de agregar el reemplazo
    usuario_existente = next((user for user in usuarios if user['id_User'] == request.json['id_User']), None)
    if not usuario_existente:
        return jsonify({'error': 'El usuario especificado no existe'}), 400

    # Verificar si el auto existe antes de agregar el reemplazo
    auto_existente = next((car for car in autos if car['patente'] == request.json['patente']), None)
    if not auto_existente:
        return jsonify({'error': 'El auto especificado no existe'}), 400

    nuevo_reemplazo = {
        'id_replace': len(reemplazos) + 1,
        'id_User': request.json['id_User'],
        'patente': request.json['patente'],
        'descripcion': request.json['descripcion'],
        'tiempo_inicio': request.json['tiempo_inicio'],
        'desde': request.json['desde'],
        'hasta': request.json['hasta'],
        'partCar': request.json['partCar']
    }
    reemplazos.append(nuevo_reemplazo)
    return jsonify({'mensaje': 'Reemplazo agregado correctamente', 'reemplazo': nuevo_reemplazo}), 201

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json  # Importa el módulo json

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Randomdev90:R$T$g4t4@Randomdev90.mysql.pythonanywhere-services.com/Randomdev90$Registros'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))
    tel = db.Column(db.String(45))
    email = db.Column(db.String(45))
    tipo = db.Column(db.String(45))
    cantidad = db.Column(db.Integer)
    entrada = db.Column(db.String(45))
    salida = db.Column(db.String(45))
    dni = db.Column(db.String(45))

    def __init__(self, nombre, tel, email, tipo, cantidad, entrada, salida, dni):
        self.nombre = nombre
        self.tel = tel
        self.email = email
        self.tipo = tipo
        self.cantidad = cantidad
        self.entrada = entrada
        self.salida = salida
        self.dni = dni

with app.app_context():
    db.create_all()

class RegistroSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'tel', 'email', 'tipo', 'cantidad', 'entrada', 'salida', 'dni')

registro_schema = RegistroSchema()
registros_schema = RegistroSchema(many=True)

@app.route('/registros', methods=['GET'])
def get_registros():
    all_registros = Registro.query.all()
    result = registros_schema.dump(all_registros)
    return jsonify(result)

@app.route('/registros/<id>', methods=['GET'])
def get_registro(id):
    registro = Registro.query.get(id)
    return registro_schema.jsonify(registro)

@app.route('/registros/<id>', methods=['DELETE'])
def delete_registro(id):
    registro = Registro.query.get(id)
    db.session.delete(registro)
    db.session.commit()
    return registro_schema.jsonify(registro)

@app.route('/registros', methods=['POST'])
def create_registro():
    # Cambia request.json a json.loads(request.form.to_dict())
    form_data = json.loads(json.dumps(request.form.to_dict(flat=True)))
    
    nombre = form_data['nombre']
    tel = form_data['tel']
    email = form_data['email']
    tipo = form_data['tipo']
    cantidad = form_data['cantidad']
    entrada = form_data['entrada']
    salida = form_data['salida']
    dni = form_data['dni']
    
    new_registro = Registro(nombre, tel, email, tipo, cantidad, entrada, salida, dni)
    db.session.add(new_registro)
    db.session.commit()
    
    return registro_schema.jsonify(new_registro)

@app.route('/registros/<id>', methods=['PUT'])
def update_registro(id):
    registro = Registro.query.get(id)

    # Cambia request.json a json.loads(request.form.to_dict())
    form_data = json.loads(json.dumps(request.form.to_dict(flat=True)))

    nombre = form_data['nombre']
    tel = form_data['tel']
    email = form_data['email']
    tipo = form_data['tipo']
    cantidad = form_data['cantidad']
    entrada = form_data['entrada']
    salida = form_data['salida']
    dni = form_data['dni']

    registro.nombre = nombre
    registro.tel = tel
    registro.email = email
    registro.tipo = tipo
    registro.cantidad = cantidad
    registro.entrada = entrada
    registro.salida = salida
    registro.dni = dni

    db.session.commit()
    return registro_schema.jsonify(registro)

# Para ejecución en localhost
if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Esta subida a pythonanywhere http://randomdev90.pythonanywhere.com
# @app.route('/')
# def hello_world():
#     return 'Hello from Flask!'

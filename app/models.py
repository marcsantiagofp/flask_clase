from . import db
from datetime import datetime


# Modelos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    vehiculo = db.relationship('Vehiculo', backref='owner', lazy=True, uselist=False)

def __repr__(self):
        return f'<User {self.username}>'

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(120), nullable=True)
    modelo = db.Column(db.String(120), nullable=True)
    matricula = db.Column(db.String(120), nullable=True)
    tipo = db.Column(db.String(120), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Parking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Plaza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(20), nullable=False, default='libre')
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Relación con el modelo User
    user = db.relationship('User', backref=db.backref('plazas', lazy=True))

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(120), nullable=False)
    fecha_entrada = db.Column(db.DateTime)
    fecha_salida = db.Column(db.DateTime, nullable=True)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# Formulario de login
class LoginForm(FlaskForm):
    username = StringField('Nom d\'usuari', validators=[DataRequired()])
    password = PasswordField('Contrasenya', validators=[DataRequired()])
    submit = SubmitField('Iniciar sessió')

# Formulario de registro
class RegisterForm(FlaskForm):
    username = StringField('Nom d\'usuari', validators=[DataRequired(), Length(min=4, max=100)])
    password = PasswordField('Contrasenya', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirma la contrasenya', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar-se')

class UpdateUserForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellidos = StringField('Apellidos', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    marca = StringField('Marca')
    modelo = StringField('Modelo')
    matricula = StringField('Matrícula')
    tipo_vehiculo = SelectField('Tipo de Vehículo', choices=[('coche', 'Coche'), ('moto', 'Moto'), ('bicicleta', 'Bicicleta')])

class PasswordChangeForm(FlaskForm):
    nueva_contrasena = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=6)])
    confirmar_contrasena = PasswordField('Confirmar Contraseña', validators=[DataRequired()])


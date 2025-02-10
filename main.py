from flask import Flask, request, make_response, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from app import create_app
from app.forms import LoginForm, RegisterForm

app = create_app()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definición de la clase User para la base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relación con Vehiculo
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

# Ruta para la página principal (inicio de sesión y registro)
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_ip' not in session:
        user_ip_information = request.remote_addr
        session["user_ip"] = user_ip_information
        return redirect('/')
    
    user_ip = session.get("user_ip")
    username = session.get("username")

    login_form = LoginForm()
    register_form = RegisterForm()

    # Si el formulario de inicio de sesión es enviado
    if login_form.validate_on_submit():
        username_input = login_form.username.data
        password_input = login_form.password.data
        
        user = User.query.filter_by(username=username_input).first()
        
        if user and check_password_hash(user.password, password_input):
            session["username"] = username_input
            flash("Has iniciat sessió correctament.")
            return redirect('/')
        else:
            flash("Nom d'usuari o contrasenya incorrectes.")
    
    # Si el formulario de registro es enviado
    if register_form.validate_on_submit():
        username_input = register_form.username.data
        password_input = register_form.password.data
        
        existing_user = User.query.filter_by(username=username_input).first()
        if existing_user:
            flash("Ja existeix un usuari amb aquest nom.")
        else:
            hashed_password = generate_password_hash(password_input)
            new_user = User(username=username_input, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Usuari creat correctament! Ara pots iniciar sessió.")
            return redirect('/')

    context = {
        'ip': user_ip,
        'login_form': login_form,
        'register_form': register_form,
        'username': username
    }

    return render_template("inicio.html", **context)

# Ruta para la página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        apellido = form.apellido.data
        email = form.email.data
        telefono = form.telefono.data
        password = form.password.data

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Ja existeix un usuari amb aquest nom o email.")
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, apellido=apellido, email=email, telefono=telefono, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Usuari creat correctament! Ara pots iniciar sessió.")
            return redirect(url_for('login'))

    return render_template('Registro.html', register_form=form)

# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Crear el formulario aquí

    if form.validate_on_submit():  # Si el formulario es válido
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            flash('Inicio de sesión exitoso!')
            return redirect(url_for('index'))  # Redirigir a la página principal
        else:
            flash('Nombre de usuario o contraseña incorrectos.')

    return render_template('Inicio_Sesion.html', form=form)  # Pasar el formulario a la plantilla

# Cerrar session
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Has cerrado sesión correctamente.")
    return redirect(url_for('index'))  # Redirige a la página de inicio

# Ruta para la página de Parkings
@app.route('/parkings')
def parkings():
    if 'username' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    
    # Obtener el nombre de usuario desde la sesión
    username = session.get('username')

    # Si estás usando un objeto 'user' basado en el nombre de usuario, puedes buscarlo en la base de datos
    user = User.query.filter_by(username=username).first()  # Ajusta según el nombre de tu modelo

    return render_template('Parking.html', user=user)


# Ruta para la página de información del usuario
@app.route('/info_usuario', methods=['GET', 'POST'])
def info_usuario():
    if 'username' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        flash("Usuario no encontrado.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Procesar los datos enviados según la sección
        if request.form.get('seccion') == 'usuario':
            nombre = request.form.get('nombre')
            apellidos = request.form.get('apellidos')
            email = request.form.get('email')
            telefono = request.form.get('telefono')
            
            if nombre:
                user.username = nombre
            if apellidos:
                user.apellido = apellidos
            if email:
                user.email = email
            if telefono:
                user.telefono = telefono

            db.session.commit()
            flash("Información del usuario actualizada correctamente.")

        elif request.form.get('seccion') == 'vehiculo':
            marca = request.form.get('marca')
            modelo = request.form.get('modelo')
            matricula = request.form.get('matricula')
            tipo = request.form.get('tipo')
            
            # Verificar si hay un vehículo asociado al usuario
            if marca or modelo or matricula or tipo:
                if not user.vehiculo:
                    # Insertar un nuevo vehículo si no existe
                    vehiculo = Vehiculo(
                        marca=marca,
                        modelo=modelo,
                        matricula=matricula,
                        tipo=tipo,
                        user_id=user.id
                    )
                    db.session.add(vehiculo)
                    flash("Información del vehículo guardada correctamente.")
                else:
                    # Si ya existe un vehículo, actualiza los datos
                    vehiculo = user.vehiculo
                    if marca:
                        vehiculo.marca = marca
                    if modelo:
                        vehiculo.modelo = modelo
                    if matricula:
                        vehiculo.matricula = matricula
                    if tipo:
                        vehiculo.tipo = tipo
                    flash("Información del vehículo actualizada correctamente.")

            db.session.commit()

        elif request.form.get('seccion') == 'contrasena':
            nueva_contrasena = request.form.get('nueva-contrasena')
            confirmar_contrasena = request.form.get('confirmar-contrasena')

            if nueva_contrasena and nueva_contrasena == confirmar_contrasena:
                user.password = generate_password_hash(nueva_contrasena)
                db.session.commit()
                flash("Contraseña actualizada correctamente.")
            else:
                flash("Las contraseñas no coinciden.")

    context = {
        "user": user
    }
    return render_template('Info_Usuario.html', **context)

# Ruta para borrar usuario
@app.route('/borrar_usuario', methods=['POST'])
def borrar_usuario():
    if 'username' not in session:
        flash("Debes iniciar sesión para realizar esta acción.")
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        flash("Usuario no encontrado.")
        return redirect(url_for('info_usuario'))

    db.session.delete(user)
    db.session.commit()
    session.pop('username', None)
    flash("Tu cuenta ha sido eliminada correctamente.")
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=81, debug=True)
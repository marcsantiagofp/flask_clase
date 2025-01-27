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
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return '<User %r>' % self.username

# Ruta para la página principal (inicio de sesión y registro)
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_ip' not in session:
        user_ip_information = request.remote_addr
        session["user_ip"] = user_ip_information
        # flash("Sessió iniciada. El teu IP s'ha registrat.")
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
    register_form = RegisterForm()

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
            return redirect(url_for('index'))

    return render_template('Registro.html', register_form=register_form)

# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Crear el formulario aquí

    if form.validate_on_submit():  # Si el formulario es válido
        username = form.username.data
        password = form.password.data

        # Aquí debería ir tu lógica de validación para verificar si el usuario existe
        # y si la contraseña es correcta
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
    # Eliminar 'username' de la sesión para cerrar la sesión
    session.pop('username', None)
    flash("Has cerrado sesión correctamente.")
    return redirect(url_for('index'))  # Redirige a la página de inicio

# Ruta para la página de Parkings
@app.route('/parkings')
def parkings():
    return render_template('parkings.html')

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
        # Recoger datos del formulario enviado
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        matricula = request.form.get('matricula')
        tipo_vehiculo = request.form.get('tipo-vehiculo')
        nueva_contrasena = request.form.get('nueva-contrasena')
        confirmar_contrasena = request.form.get('confirmar-contrasena')

        # Validar y actualizar contraseña
        if nueva_contrasena and nueva_contrasena == confirmar_contrasena:
            user.password = generate_password_hash(nueva_contrasena)
            db.session.commit()
            flash("Contraseña actualizada correctamente.")
        elif nueva_contrasena or confirmar_contrasena:
            flash("Las contraseñas no coinciden o están vacías.")

        # Guardar otros cambios (si es necesario)
        # Aquí puedes procesar la lógica para guardar más datos en la base de datos

        flash("Los cambios han sido guardados.")

    # Pasar los datos del usuario actual a la plantilla
    context = {
        "username": user.username,
        # Añadir aquí información adicional que quieras mostrar en la plantilla
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
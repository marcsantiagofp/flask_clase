from flask import Flask, request, make_response, redirect, render_template, session, flash, url_for, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import LoginForm, RegisterForm
from .models import User, Vehiculo, Log, Parking, Plaza
from . import db
from datetime import datetime
import requests

def register_routes(app):
    from app.models import User, db
    # PAGINA PRINCIPAL
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

    # USUARIOS 
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
        form = LoginForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['username'] = username
                flash('Inicio de sesión exitoso!')
                return redirect(url_for('index'))
            else:
                flash('Nombre de usuario o contraseña incorrectos.')

        return render_template('Inicio_Sesion.html', form=form)

    # Cerrar session
    @app.route('/logout')
    def logout():
        session.pop('username', None)
        flash("Has cerrado sesión correctamente.")
        return redirect(url_for('index'))

    # INFORMACION USUARIO
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


    # PAGINA PARKINGS
    @app.route('/parkings', methods=['GET', 'POST'])
    def parkings():
        if 'username' not in session:
            flash("Debes iniciar sesión para acceder a esta página.")
            return redirect(url_for('login'))  

        user = User.query.filter_by(username=session['username']).first()
        if not user:
            flash("Usuario no encontrado.")
            return redirect(url_for('login'))

        # Obtener todos los parkings
        parkings = Parking.query.all()
        parking_data = {}

        for parking in parkings:
            parking_data[parking.id] = {
                "title": f"Mapa del {parking.nombre}",
                "infoTitle": parking.nombre,
                "free": 0,
                "occupied": 0,
                "reserved": 0,
                "slots": []
            }

            plazas = Plaza.query.filter_by(parking_id=parking.id).all()
            
            for plaza in plazas:
                plaza_data = {
                    "id": plaza.id,
                    "status": plaza.estado
                }

                if plaza.estado == 'libre':
                    parking_data[parking.id]["free"] += 1
                elif plaza.estado == 'ocupada':
                    parking_data[parking.id]["occupied"] += 1
                elif plaza.estado == 'reservada':
                    parking_data[parking.id]["reserved"] += 1

                parking_data[parking.id]["slots"].append(plaza_data)

        # 🛠️ Depuración: Imprimir los datos recogidos en la terminal
        print("Datos de parkings y plazas:", parking_data)

        # Procesar la reserva de plaza
        if request.method == 'POST':
            plaza_id = request.form.get('plaza_id')
            print("ID de plaza seleccionada:", plaza_id)

            plaza = Plaza.query.filter_by(id=plaza_id).first()
            print("Plaza encontrada en BD:", plaza)

            if plaza and plaza.estado == 'libre':
                plaza.estado = 'reservada'
                plaza.user_id = user.id
                db.session.commit()
                flash("Plaza reservada correctamente.")
                print(f" Plaza {plaza_id} reservada para el usuario {user.username}")
                return redirect(url_for('parkings'))
            else:
                flash("La plaza no está disponible para la reserva.")
                print("La plaza no estaba disponible.")

        context = {
            'user': user,
            'parkings': parking_data
        }
        return render_template("Parking.html", **context)


    # ESP 32

    ESP32_URL = 'http://172.16.6.200/abrir_barrera'

    @app.route('/api/entrada', methods=['POST'])
    def entrada():
        data = request.get_json(force=True)
        matricula = data.get('matricula')

        vehiculo = Vehiculo.query.filter_by(matricula=matricula).first()
        if not vehiculo:
            return jsonify({'error': 'Matrícula no encontrada'}), 403

        log = Log.query.filter_by(matricula=matricula, fecha_salida=None).first()
        
        if log:
            # Procesar salida
            log.fecha_salida = datetime.now()

            plaza = Plaza.query.filter_by(user_id=vehiculo.user_id, estado='ocupada').first()
            if plaza:
                plaza.estado = 'libre'
                plaza.user_id = None

            db.session.commit()
            return jsonify({
                "message": "Salida registrada, hasta luego",
                "matricula": matricula,
                "hora_salida": log.fecha_salida.strftime('%Y-%m-%d %H:%M:%S')
            }), 200
        else:
            # Procesar entrada
            plazaLibre = Plaza.query.filter_by(estado='libre').first()
            if plazaLibre:
                nuevo_log = Log(matricula=matricula, fecha_entrada=datetime.now())
                db.session.add(nuevo_log)

                plazaLibre.estado = 'ocupada'
                plazaLibre.user_id = vehiculo.user_id

                db.session.commit()

                return jsonify({
                    "message": "Entrada registrada, Bienvenido",
                    "matricula": matricula
                }), 200
            else:
                return jsonify({'error': 'No hay plazas disponibles'}), 409

    @app.route('/api/actualizaSpot', methods=['POST'])
    def actualizaSpot():
        try:
            data = request.get_json(force=True)
            plaza_id = data.get('plazaId')
            estado = data.get('estado')

            # Validar entrada
            if not plaza_id or not estado:
                return jsonify({'error': 'Faltan datos requeridos'}), 400
            
            if estado not in ['libre', 'ocupada', 'reservada']:
                return jsonify({'error': 'Estado inválido'}), 400

            plaza = Plaza.query.filter_by(id=plaza_id).first()
            if not plaza:
                return jsonify({'error': 'Plaza no encontrada'}), 404

            # Actualizar estado y user_id si aplica
            plaza.estado = estado
            if estado == 'libre':
                plaza.user_id = None  # Liberar la plaza

            db.session.commit()

            return jsonify({
                'message': 'Plaza actualizada correctamente',
                'plazaId': plaza_id,
                'estado': estado
            }), 200

        except Exception as e:
            return jsonify({'error': f'Error interno: {str(e)}'}), 500

    
    def abrir_barrera():
        try:
            response = requests.post(ESP32_URL, json={"accion": "abrir"}, timeout=5)
            if response.status_code == 200:
                print("Barrera abierta correctamente.")
                return True
            else:
                print(f"Error al activar la barrera: Código {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"Error al comunicarse con la ESP32: {e}")
            return False
    
    



class Config:
    SECRET_KEY = "CLAVE SEGURA"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/flask_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
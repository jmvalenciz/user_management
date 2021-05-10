from flask_sqlalchemy import SQLAlchemy

class DB:
    def __init__(self, app):
        self.database = 'agendatorio'
        self.hostname = 'example.com'
        self.port = '3306'
        self.username = 'agendatorio'
        self.password = 'agendatorio'

        app.config['SECRET_KEY'] = '6hCSafxoaRxMCNzYbKg9Lmw3hSHKcGbN'
        uri = 'mysql://' + self.username + ':' + self.password
        uri += '@' + self.hostname + ':' + self.port
        uri += '/' + self.database
        app.config['SQLALCHEMY_DATABASE_URI'] = uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db = SQLAlchemy(app)


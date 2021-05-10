from flask import Flask, request, make_response
from db import DB
import jwt
from functools import wraps

app = Flask(__name__)
db = DB(app)


class Usuario(db.db.Model):
    __tablename__ = 'Usuario'
    idUsuario = db.db.Column(db.db.Integer, primary_key=True)
    email = db.db.Column(db.db.String(45))
    password = db.db.Column(db.db.String(50))
    nombre = db.db.Column(db.db.String(45))

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return {
                'error': 1,
                'msg': 'No se encontro el token'
            }, 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Usuario.query.filter_by(idUsuario=data['idUsuario']).first()
        except:
            return {
                'error': 2,
                'msg': 'El token no es valido'
            }, 401
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/login', methods=['POST'])
def login():

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('No se pudo verificar', 401, {'WWW-Authenticate': 'Basic realm="Login requerido"'})
    
    user = Usuario.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('No se pudo verificar', 401, {'WWW-Authenticate': 'Basic realm="Login requerido"'})
    
    if not (user.password == auth.password):
        return make_response('No se pudo verificar', 401, {'WWW-Authenticate': 'Basic realm="Login requerido"'})
    
    token = jwt.encode({'idUsuario':user.idUsuario}, app.config['SECRET_KEY'], algorithms=["HS256"])
    return{
        'error': 0,
        'token': token
    }


@app.route('/register', methods=['POST'])
def register_user():
    context = request.json
    new_user = Usuario(
        email=context['email'],
        password=context['password'],
        nombre=context['nombre'])

    db.db.session.add(new_user)
    db.db.session.commit()
    return {
        'error': 0,
        'msg': 'Usuario registrado correctamente'
    }

@app.route('/user', methods=['POST'])
@token_required
def edit_user(current_user):
    context = request.json
    if 'email' in context:
        current_user.email = context['email']
    if 'password' in context:
        current_user.password = context['password']
    if 'nombre' in context:
        current_user.password = context['nombre']
    
    db.db.session.commit()

@app.route('/user', methods=['DELETE'])
@token_required
def delete_user(current_user):
    if current_user is None:
        return {
            'error': 1,
            'msg': 'EL usuario no existe'
        }
    db.db.session.delete(current_user)
    db.db.session.commit()
    return{
        'error': 0,
        'msg': 'Se ha eliminado el usuario'
    }

if __name__ == "__main__":
    app.run(debug=True)
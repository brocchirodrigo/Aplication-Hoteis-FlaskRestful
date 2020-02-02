from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
import traceback
from flask import make_response, render_template

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='Campo usuário obrigatório')
atributos.add_argument('senha', type=str, required=True, help='Campo senha é obrigatório')
atributos.add_argument('email', type=str)
atributos.add_argument('ativado', type=bool)

class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                 return {'message': 'Erro ao tentar deletar o usuário no banco de dados.'}, 500 #internal server error       
            return {'message': 'User deleted.'}, 200
        return {'message': 'User not found.'}, 404

class UserRegister(Resource):
    
    def post(self):
        
        dados = atributos.parse_args()
        if not dados.get('email') or dados.get('email') is None:
            return {'message': 'O campo email não pode ser deixado em branco.'}, 400

        if UserModel.find_by_email(dados['email']):
            return {'message': 'O email '"'{}'"' já se encontra cadastrado.'.format(dados['email'])}, 400

        if UserModel.find_by_user(dados['login']):
            return {'message': 'O login '"'{}'"' já existe.'.format(dados['login'])}
        
        user = UserModel(**dados)
        user.ativado = False
        try:
            user.save_user()
            user.enviarconfirmacao()
        except:
            user.delete_user()
            traceback.print_exc()
            return {'message': 'Internal server error.'}, 500
        return {'message': 'Usuário criado com sucesso.'}, 201
    
class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        
        user = UserModel.find_by_user(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            if user.ativado:
                token_de_acesso = create_access_token(identity=user.user_id)
                return {'access_token': token_de_acesso}, 200
            return {'message': 'Usuário não confirmado.'}, 400
        return {'message': 'Usuário ou senha incorretos'}, 401
    
class UserLogout(Resource):
    
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logout com sucesso'}, 200

class UserConfirm(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)
    
        if not user:
            return {'message': 'Usuário id '"'{}'"' não encontrado.'.format(user_id)}, 404

        user.ativado = True
        user.save_user()
        headers = {'content-type': 'text/html'}
        return make_response(render_template('confirmacao.html', email=user.email, usuario=user.login), 200, headers)


        #return {'message': 'Usuário id '"'{}'"' confirmado com sucesso.'.format(user_id)}, 200

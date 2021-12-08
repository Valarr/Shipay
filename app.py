from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import random
import string


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#conmfigurar para os parametros locais no formato: dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3310/shipay'
db = SQLAlchemy(app)

#resposta 2
#modelo do banco
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)
    claims = db.relationship('Claims', secondary="user_claims")
    role = db.relationship('Roles')

    #converte para json
    def to_json(self):
        return {"id":self.id,
                "name":self.name,
                "email":self.email,
                "password":self.password,
                "role_id":self.role_id,
                "created_at":self.created_at,
                "updated_at":self.updated_at,
                "claims":[claim.to_json() for claim in self.claims],
                "role":self.role.to_json()}

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(45), nullable=False)

    #converte para json
    def to_json(self):
        return {"id":self.id,
                "description":self.description}

class Claims(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(45), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    #converte para json
    def to_json(self):
        return {"id":self.id,
                "description":self.description,
                "active":self.active}

class User_claims(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    claim_id=db.Column(db.Integer, db.ForeignKey('claims.id'))

    #converte para json
    def to_json(self):
        return {"id":self.id,
                "user_id":self.user_id,
                "claim_id":self.claim_id}

#Cria o banco de dados no esquema acima
#Necessario rodar uma vez
#db.create_all()

#Gerador de senhas aleatorias
def get_random_password():
    # escolhe entre todas as letras em caixa baixa
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(8))
    return result_str

#CRUD
#Retorna todos os usuarios
@app.route('/')
def retorna_todos_usuarios():
    #users_obj = Users.query.with_entities(Users.name, Users.email, Users.role, Users.claims).all()
    #users_json = [Users for Users in users_obj]
    user_obj = Users.query.all()
    user_obj_json = [Users.to_json() for Users in user_obj]
    json_final = []
    for i in range(len(user_obj_json)):
        claim = []
        for j in range(len(user_obj_json[i]["claims"])):
            claim.append(user_obj_json[i]["claims"][j]["description"])
        json_final.append({"name":user_obj_json[i]["name"],
                            "email":user_obj_json[i]["email"],
                            "descricao_permissao":user_obj_json[i]["role"]["description"],
                            "descricao_claim":claim})
                            
    return response_gen(200,"Users",json_final,"OK")

#resposta 3
#seleciona por id
@app.route("/user_role/<id>", methods=["GET"])
def seleciona_usuario_por_id(id):
    #retorna o valor que coresponde ao mesmo id passado
    users_obj = Users.query.filter_by(id=id).first()
    users_json = users_obj.to_json()

    #retorna o json para a requisicao
    return response_gen(200,"Role description",users_json["role"]["description"])

#resposta 4
#Cria novo usuario
@app.route("/new_user", methods=["POST"])
def adiciona_usuario():
    body = request.get_json()
    #validar se veio os parametros
    try:
        if "password" not in body or body["password"] == "":
            body["password"] = str(get_random_password())
        #cria um veiculo
        date_today = datetime.today().strftime('%Y-%m-%d')
        user = Users( name=body["name"],
                    email=body["email"],
                    password=body["password"],
                    role_id=body["role_id"],
                    created_at=date_today)
        #abre uma secao e adicionou a classe
        db.session.add(user)
        db.session.commit()

        return response_gen(201,"Users",str(user.to_json()),"Adicionado")
    except Exception as e:
        print(e)

        return response_gen(400,"Users",{},"Erro ao adicionar")

#padronizando os retornos
def response_gen(status, content_name, content,message=False):
    body = {}
    body[content_name] = content
    
    if(message):
        body["message"] = message

    return Response(json.dumps(body),status=status, mimetype="application/json")

if __name__ == '__main__':
    app.run()
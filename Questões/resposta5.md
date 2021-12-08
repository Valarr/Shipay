
## Descrição

Para solucionar o desafio, foram escolhidas as bibliotecas do Python🐍:
Flask e Flask_sqlalchemy

Como o sistema não foi contenarizado, é necessario que se utilize um banco local, nos modelos do que foi fornecido de base, no arquivo bancoMSQ.sql, existe um modelo de como foi estruturado o banco de dados utilizando o MySQL.

## Dependencias

Para instalar as dependencias basta executar o comando na raiz do projeto:

```
$ pip install -r requirements.txt
```

## Rodar projeto

Para executar o projeto, estando na raiz do projeto, basta executar o comando no terminal:

```
$ python app.py
```

## Funcionalidades

Essa seção explica/exemplifica como testar/executar as funcionalidades do projeto.

Além dos comandos CURL é possivel chamar os endpoints usando o Insomnia ou Postman.

### Consultar todos os usuarios

```
$ curl http://localhost:5000
```

### Consultar a role do usuario por id

```
$ curl curl http://localhost:5000/user_role/{id}
```

### Criar um novo usuario

```
$ curl http://localhost:5000/new_user
no modelo de POST:
{
    "name": "string",
    "email": "string",
    "password": "string", //Caso não seja fornecida, o sistega ira gerar uma aleatoria
    "role_id": "int"
  }
```

### Deploy

O deploy da aplicação pode ser feito apos dockerizar o sistema atravez de um arquivo docker-compose e um arquivo docker com as instruções para subir a imagem, sendo necessario configurar a conexão com o banco de dados para funcionar como planejado, visto que essa arquitetura simples foi utilizada apenas para desenvolvimento.
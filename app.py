from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger

# cria a aplicacao
app = Flask(__name__)

# ativação do CORS
CORS(app)

# configura o banco sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# configura o swagger
app.config['SWAGGER'] = {
    'title': 'GuiaGamer API',
    'uiversion': 3,
    'description': 'API para o app GuiaGamer - detonados de jogos com sistema de pistas progressivas',
    'version': '1.0.0'
}

# inicia o sqlalchemy e o swagger
db = SQLAlchemy(app)
swagger = Swagger(app)


# modelos das tabelas

class Jogo(db.Model):
    __tablename__ = 'jogos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    plataforma = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    
    # relacionamento com as etapas
    # cascade='all, delete-orphan' faz com que ao deletar um jogo, 
    # todas as etapas dele sejam deletadas tambem
    etapas = db.relationship('Etapa', backref='jogo', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'plataforma': self.plataforma,
            'descricao': self.descricao
        }


class Etapa(db.Model):
    __tablename__ = 'etapas'
    
    id = db.Column(db.Integer, primary_key=True)
    jogo_id = db.Column(db.Integer, db.ForeignKey('jogos.id'), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    pista_leve = db.Column(db.Text, nullable=False)
    pista_media = db.Column(db.Text, nullable=False)
    resposta_completa = db.Column(db.Text, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'jogo_id': self.jogo_id,
            'numero': self.numero,
            'titulo': self.titulo,
            'pista_leve': self.pista_leve,
            'pista_media': self.pista_media,
            'resposta_completa': self.resposta_completa
        }


# rotas da api

@app.route('/')
def home():
    """
    Rota inicial da API
    ---
    tags:
      - Home
    responses:
      200:
        description: Informacoes basicas da API
    """
    return jsonify({
        "mensagem": "Bem-vindo a API do GuiaGamer!",
        "versao": "1.0",
        "status": "online",
        "documentacao": "/apidocs"
    })


@app.route('/listar_jogos', methods=['GET'])
def listar_jogos():
    """
    Lista todos os jogos cadastrados
    ---
    tags:
      - Jogos
    responses:
      200:
        description: Lista de jogos retornada com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              plataforma:
                type: string
              descricao:
                type: string
    """
    jogos = Jogo.query.all()
    jogos_lista = [jogo.to_dict() for jogo in jogos]
    return jsonify(jogos_lista)


@app.route('/cadastrar_jogo', methods=['POST'])
def cadastrar_jogo():
    """
    Cadastra um novo jogo
    ---
    tags:
      - Jogos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
            - plataforma
          properties:
            nome:
              type: string
              example: "Pokemon FireRed"
            plataforma:
              type: string
              example: "Game Boy Advance"
            descricao:
              type: string
              example: "RPG classico de Pokemon"
    responses:
      201:
        description: Jogo cadastrado com sucesso
      400:
        description: Dados invalidos (nome ou plataforma faltando)
    """
    dados = request.get_json()
    
    if not dados or not dados.get('nome') or not dados.get('plataforma'):
        return jsonify({
            "erro": "Nome e plataforma sao obrigatorios"
        }), 400
    
    novo_jogo = Jogo(
        nome=dados['nome'],
        plataforma=dados['plataforma'],
        descricao=dados.get('descricao')
    )
    
    db.session.add(novo_jogo)
    db.session.commit()
    
    return jsonify({
        "mensagem": "Jogo cadastrado com sucesso!",
        "jogo": novo_jogo.to_dict()
    }), 201


@app.route('/buscar_jogo/<int:id>', methods=['GET'])
def buscar_jogo(id):
    """
    Busca um jogo especifico pelo ID
    ---
    tags:
      - Jogos
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do jogo
    responses:
      200:
        description: Jogo encontrado
      404:
        description: Jogo nao encontrado
    """
    jogo = Jogo.query.get(id)
    
    if not jogo:
        return jsonify({"erro": "Jogo nao encontrado"}), 404
    
    return jsonify(jogo.to_dict())


@app.route('/deletar_jogo/<int:id>', methods=['DELETE'])
def deletar_jogo(id):
    """
    Deleta um jogo pelo ID
    ---
    tags:
      - Jogos
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do jogo a deletar
    responses:
      200:
        description: Jogo deletado com sucesso
      404:
        description: Jogo nao encontrado
    """
    jogo = Jogo.query.get(id)
    
    if not jogo:
        return jsonify({"erro": "Jogo nao encontrado"}), 404
    
    db.session.delete(jogo)
    db.session.commit()
    
    return jsonify({
        "mensagem": f"Jogo '{jogo.nome}' deletado com sucesso!"
    })


@app.route('/cadastrar_etapa', methods=['POST'])
def cadastrar_etapa():
    """
    Cadastra uma nova etapa para um jogo
    ---
    tags:
      - Etapas
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - jogo_id
            - numero
            - titulo
            - pista_leve
            - pista_media
            - resposta_completa
          properties:
            jogo_id:
              type: integer
              example: 1
            numero:
              type: integer
              example: 1
            titulo:
              type: string
              example: "Escolher o Pokemon inicial"
            pista_leve:
              type: string
              example: "Voce precisa visitar um lugar importante"
            pista_media:
              type: string
              example: "Va ao laboratorio do Professor"
            resposta_completa:
              type: string
              example: "Va ao laboratorio em Pallet Town e escolha um Pokemon"
    responses:
      201:
        description: Etapa cadastrada com sucesso
      400:
        description: Dados invalidos
      404:
        description: Jogo nao encontrado
    """
    dados = request.get_json()
    
    campos_obrigatorios = ['jogo_id', 'numero', 'titulo', 'pista_leve', 'pista_media', 'resposta_completa']
    for campo in campos_obrigatorios:
        if not dados or not dados.get(campo):
            return jsonify({
                "erro": f"O campo '{campo}' eh obrigatorio"
            }), 400
    
    jogo = Jogo.query.get(dados['jogo_id'])
    if not jogo:
        return jsonify({"erro": "Jogo nao encontrado"}), 404
    
    nova_etapa = Etapa(
        jogo_id=dados['jogo_id'],
        numero=dados['numero'],
        titulo=dados['titulo'],
        pista_leve=dados['pista_leve'],
        pista_media=dados['pista_media'],
        resposta_completa=dados['resposta_completa']
    )
    
    db.session.add(nova_etapa)
    db.session.commit()
    
    return jsonify({
        "mensagem": "Etapa cadastrada com sucesso!",
        "etapa": nova_etapa.to_dict()
    }), 201


@app.route('/listar_etapas/<int:jogo_id>', methods=['GET'])
def listar_etapas(jogo_id):
    """
    Lista todas as etapas de um jogo especifico
    ---
    tags:
      - Etapas
    parameters:
      - in: path
        name: jogo_id
        type: integer
        required: true
        description: ID do jogo
    responses:
      200:
        description: Lista de etapas retornada com sucesso
      404:
        description: Jogo nao encontrado
    """
    jogo = Jogo.query.get(jogo_id)
    if not jogo:
        return jsonify({"erro": "Jogo nao encontrado"}), 404
    
    etapas = Etapa.query.filter_by(jogo_id=jogo_id).order_by(Etapa.numero).all()
    etapas_lista = [etapa.to_dict() for etapa in etapas]
    
    return jsonify(etapas_lista)


@app.route('/deletar_etapa/<int:id>', methods=['DELETE'])
def deletar_etapa(id):
    """
    Deleta uma etapa pelo ID
    ---
    tags:
      - Etapas
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da etapa a deletar
    responses:
      200:
        description: Etapa deletada com sucesso
      404:
        description: Etapa nao encontrada
    """
    etapa = Etapa.query.get(id)
    
    if not etapa:
        return jsonify({"erro": "Etapa nao encontrada"}), 404
    
    db.session.delete(etapa)
    db.session.commit()
    
    return jsonify({
        "mensagem": "Etapa deletada com sucesso!"
    })


# inicializa o servidor

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, port=5000)

# GuiaGamer - API (Back-end)

API REST do projeto **GuiaGamer**, um app web que oferece detonados de jogos com sistema de pistas progressivas para evitar spoilers indesejados.

Esta é a parte do back-end do projeto. O front-end está em outro repositório.

## Sobre o projeto

O GuiaGamer nasceu pra resolver alguns problemas comuns dos gamers ao consultar detonados online:

- Exposição a spoilers de partes do jogo que o jogador ainda não chegou
- Dificuldade de lembrar exatamente onde parou no detonado
- Necessidade de consultar diferentes sites dependendo do jogo

Para evitar spoilers, a API oferece um sistema de pistas em 3 níveis:

- **Dica leve**: uma sugestão sutil, sem entregar a resposta
- **Dica direta**: orientação mais clara
- **Passo completo**: a resposta detalhada

Assim, o jogador escolhe quanto quer revelar a cada momento.

Além disso, o app permite marcar etapas como concluídas, ajudando o jogador a acompanhar seu progresso e retomar de onde parou.

No futuro, a ideia é que o site funcione como um "wikipedia" em que temos um sistema de login e que os usuarios podem cadastrar os jogos e detonados e fazerem sugestões de ajustes quando preferirem.

## Tecnologias usadas

- Python 3.11
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- Flasgger
- SQLite

## Como instalar e rodar

### Pré-requisitos

- Python 3.11 ou superior

### Passo a passo

1. Clonar o repositório:

```
git clone https://github.com/fredericwithc/guiagamer-be.git
cd guiagamer-be
```

2. Criar o ambiente virtual:

```
python -m venv venv
```

3. Ativar o ambiente virtual:

```
venv\Scripts\activate
```

4. Instalar as dependências:

```
pip install -r requirements.txt
```

5. Rodar o servidor:

```
python app.py
```

A API vai estar rodando em `http://localhost:5000`

## Documentação da API

Com o servidor rodando, você pode acessar `http://localhost:5000/apidocs` pra ver a documentação completa no Swagger.

## Rotas disponíveis

### Jogos

- `GET /listar_jogos` - lista todos os jogos
- `POST /cadastrar_jogo` - cadastra um novo jogo
- `GET /buscar_jogo/<id>` - busca um jogo pelo id
- `DELETE /deletar_jogo/<id>` - deleta um jogo

### Etapas

- `POST /cadastrar_etapa` - cadastra uma nova etapa
- `GET /listar_etapas/<jogo_id>` - lista as etapas de um jogo
- `DELETE /deletar_etapa/<id>` - deleta uma etapa

## Banco de dados

O banco tem duas tabelas com relacionamento 1:N (um jogo tem várias etapas):

**Tabela jogos:**
- id (chave primária)
- nome
- plataforma
- descricao

**Tabela etapas:**
- id (chave primária)
- jogo_id (chave estrangeira)
- numero
- titulo
- pista_leve
- pista_media
- resposta_completa

Obs: Quando um jogo é deletado, todas as suas etapas são deletadas automaticamente.

## Front-end

O front-end do projeto está em outro repositório: [guiagamer-fe](https://github.com/fredericwithc/guiagamer-fe)

## Feito por

Frederic Chomé Bombini Leyenberger - Projeto de MVP da pós-graduação da PUC-Rio

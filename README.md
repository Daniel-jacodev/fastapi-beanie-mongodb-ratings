# 🎬 MovieRate API - Sistema de Avaliações de Mídias

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Beanie](https://img.shields.io/badge/Beanie_ODM-FF6F61?style=for-the-badge)

Uma API robusta desenvolvida para gestão e avaliação de mídias (filmes, desenhos e séries), utilizando **FastAPI** e o ODM assíncrono **Beanie** para integração com **MongoDB**.

## 🚀 Funcionalidades

- **CRUD Completo**: Gerenciamento de Gêneros, Usuários, Mídias e Avaliações.
- **Relacionamentos Complexos**: Uso de Links do Beanie para vincular mídias a múltiplos gêneros e avaliações a usuários/mídias.
- **Busca Avançada**: Pesquisa de mídias por título utilizando Expressões Regulares (parcial e case-insensitive).
- **Inteligência de Dados**: Ranking de mídias (Top 15) calculado em tempo real via **Aggregation Pipeline** do MongoDB.
- **Escalabilidade**: Paginação automática implementada em todas as listagens principais.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.13+
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Banco de Dados:** [MongoDB](https://www.mongodb.com/) (Atlas & Local)
- **ODM:** [Beanie](https://beanie-odm.dev/) (Object Document Mapper)
- **Validação:** [Pydantic v2](https://docs.pydantic.dev/)
- **Servidor:** Uvicorn

## 📂 Estrutura do Projeto

```text
sistema_avaliacoes/
├── app/
│   ├── core/         # Configurações de banco de dados
│   ├── models/       # Modelos Beanie (Documentos)
│   ├── routes/       # Endpoints da API (FastAPI Routers)
│   └── main.py       # Ponto de entrada da aplicação
├── .env              # Variáveis de ambiente (Atlas/Local)
├── popular_banco.py  # Script para população de dados de teste
└── requirements.txt  # Dependências do projeto

⚙️ Como Executar o Projeto
1. Clonar o repositório
git clone https://github.com/Daniel-jacodev/fastapi-beanie-mongodb-ratings.git

2. Configurar o Ambiente Virtual (Linux)python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

3. Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto:
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=sistema_avaliacoes

4. Popular o Banco de Dados
Para inserir automaticamente 21 mídias, gêneros e avaliações de teste:
PYTHONPATH=. python popular_banco.py

5. Iniciar a API
uvicorn app.main:app --reload
```

# fastapi-beanie-mongodb-ratings

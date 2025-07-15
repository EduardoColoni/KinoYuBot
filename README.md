
# 🎮 KinoYuBot – Discord Bot Integrado à Twitch com Sorteios Automatizados

KinoYuBot é um projeto pessoal desenvolvido com o objetivo de unir tecnologias modernas como Discord, Twitch, FastAPI, Redis e PostgreSQL em um sistema completo de sorteios ao vivo, com autenticação segura via OAuth2.

Este projeto representa minhas habilidades em **integrações e criação de APIs**, **autenticação segura**, **comunicação entre serviços**, e **estruturação de aplicações backend**.

---

## 🎯 Objetivo do Projeto

Desenvolver um bot de Discord capaz de:

- Autenticar um streamer da Twitch via OAuth2.
- Monitorar os espectadores ativos da live.
- Realizar sorteios automáticos de itens com base em lógica de probabilidade variável.
- Enviar notificações diretamente no Discord e twitch.

---

## ✅ Funcionalidades já implementadas

### 🔐 Autenticação via Twitch (OAuth2)
- Implementação completa do fluxo OAuth2.
- Requisição e armazenamento seguro de `access_token` e `refresh_token` no PostgreSQL.
- Callback configurado com `FastAPI` e integração ao bot via webhook.

### 🤖 Bot do Discord
- Bot funcional utilizando `discord.py` com comando `!iniciar`.
- Comunicação com backend via `requests`.
- Estrutura pronta para novos comandos e expansão.

### 🗃️ Banco de Dados
- Conexão segura com PostgreSQL usando `psycopg2`.
- Armazenamento de tokens da Twitch em formato JSON.
- Gerenciamento modular da conexão (`connect.py`).
- Configurado Redis

### 🌐 Backend com FastAPI
- API assíncrona leve com rotas organizadas.
- Rota principal de callback e pegar chatters.
- Pronto para expansão com novos endpoints (ex: /histórico, /status).

### 📡 Integração total com a API da Twitch
- Recuperação da lista de espectadores ao vivo (via API Helix ou alternativa).
- Validação e renovação de tokens expirados com `refresh_token`.

### 🎁 Sorteios com base em espectadores
- Cadastro de itens com seus pesos para sorteio separado por streamer

---

## 🚧 Funcionalidades em desenvolvimento

### 🎁 Sorteios com base em espectadores
- Agendamento de verificação periódica (a cada minuto).
- Lógica de sorteio de itens e espectadores.
- Feedback automático de sorteio no canal do Discord.

### 🔒 Segurança e Robustez
- Adição de logs, autenticações adicionais e proteção de endpoints.
- Armazenamento de histórico de sorteios.

---

## 🧰 Tecnologias Utilizadas

- **Python 3.10+**
- **Discord.py** – Bot no Discord
- **FastAPI** – Backend assíncrono para autenticação e controle
- **OAuth2** – Autenticação segura com a Twitch
- **Twitch API (Helix)** – Para monitoramento da transmissão
- **PostgreSQL** – Armazenamento seguro de tokens
- **Redis** - Armazenamento cache para o banco de dados
- **psycopg2** – Driver PostgreSQL
- **dotenv** – Variáveis de ambiente
- **ngrok** – Exposição de APIs locais para testes

---

## 📁 Estrutura de Arquivos

```
KinoYuBot/
├── .venv/                              # Ambiente virtual
├── .env                                # Variáveis de ambiente (DISCORD_TOKEN, CLIENT_ID, CLIENT_SECRET, DB_PASSWORD, REDIS_HOST, etc.)
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt                    # Dependências do projeto (discord.py, fastapi, uvicorn, python-dotenv, psycopg2, redis, requests)

├── bot/                                # Lógica do Bot Discord
│   ├── __init__.py
│   ├── main_bot.py                     # Inicialização do bot e carregamento dos cogs
│   ├── commands/                           # Comandos do bot no Discord
│   │   ├── __init__.py
│   │   └── raffle_commands.py         # Comando '!iniciar' e lógica de sorteio (em desenvolvimento)
│   └── services/                       # Comunicação com o backend FastAPI
│       ├── __init__.py
│       └── backend_api_client.py      # Cliente HTTP para interagir com o backend (get_chatters, refresh_token)

├── api/                                # Backend FastAPI
│   ├── __init__.py
│   ├── main_api.py                     # Inicialização da aplicação FastAPI
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py             # Endpoints de autenticação Twitch
│   │   └── chatters_routes.py         # Endpoint para obter os espectadores ativos
│   └── services/
│       ├── __init__.py
│       └── twitch_api_service.py      # Requisições à API da Twitch (OAuth, Helix)

├── core/                               # Módulos e configurações compartilhadas
│   ├── __init__.py
│   ├── config.py                       # Carregamento de variáveis de ambiente e configurações globais
│   └── exceptions.py                   # Exceções customizadas

├── database/
│   ├── __init__.py
│   ├── postgres/
│   │   ├── __init__.py
│   │   ├── connection_options_postgres.py  # Configurações de conexão com PostgreSQL
│   │   ├── postgres_connection.py          # Gerenciamento da conexão
│   │   └── postgres_repository.py          # Operações de CRUD para os tokens
│   └── redis/
│       ├── __init__.py
│       ├── connection_options_redis.py     # Configurações de conexão com Redis
│       ├── redis_connection.py             # Gerenciamento da conexão
│       └── redis_repository.py             # Operações de cache com Redis

```

---

## 🧪 Como Testar Localmente

1. Clone o repositório e crie o ambiente virtual:
```bash
git clone https://github.com/seu-usuario/KinoYuBot.git
cd KinoYuBot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure o `.env`:
```env
DISCORD_TOKEN=seu_token_do_discord
CLIENT_ID=seu_client_id_twitch
CLIENT_SECRET=seu_client_secret_twitch
DB_PASSWORD=senha_postgres
```

3. Execute o backend:
```bash
uvicorn main:app --reload
```

4. Execute o bot:
```bash
python bot.py
```

5. Exponha localmente com ngrok (opcional):
```bash
ngrok http 8000
```

---

## 👨‍💻 Autor

**Eduardo Coloni**  
Desenvolvedor Backend com foco em APIs, bots e integrações em tempo real.  
Tecnologias dominadas: Python, FastAPI, PostgreSQL, Discord.py, OAuth2.

---

## 📝 Licença


#Colocar depois as coisas de configuração dos bancos, teste, dev e produção#

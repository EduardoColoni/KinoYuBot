# 🎮 KinoYuBot – Discord Bot Integrado à Twitch com Sorteios Automatizados

KinoYuBot é um projeto pessoal desenvolvido com o objetivo de unir tecnologias modernas como Discord, Twitch, FastAPI, Redis e PostgreSQL em um sistema completo de sorteios ao vivo, com autenticação segura via OAuth2.

Este projeto representa minhas habilidades em **integrações e criação de APIs**, **autenticação segura**, **comunicação entre serviços**, e **estruturação de aplicações backend**.

---

## 🎯 Objetivo do Projeto

Desenvolver um bot de Discord capaz de:

- Autenticar um streamer da Twitch via OAuth2.
- Monitorar os espectadores ativos da live.
- Realizar sorteios automáticos de itens com base em lógica de probabilidade variável.
- Enviar notificações diretamente no Discord e Twitch.

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
- Uso de **Connection Pool** com `psycopg2.pool.SimpleConnectionPool`.
- Banco dividido em ambientes de **teste**, **desenvolvimento** e **produção**.
- Armazenamento de tokens da Twitch em formato JSON.
- Operações organizadas via repositórios.

### 🌐 Backend com FastAPI
- API assíncrona leve com rotas organizadas.
- Uso de **lifespan events** para inicialização do pool.
- Cada rota pega e devolve uma conexão do pool corretamente.
- Serviços desacoplados da lógica de rota.

### 📡 Integração total com a API da Twitch
- Recuperação da lista de espectadores ao vivo via Helix.
- Validação e renovação de tokens expirados com `refresh_token`.

### 🎁 Sorteios com base em espectadores
- Cadastro de itens com seus pesos para sorteio por streamer.
- Função em PostgreSQL (`make_raffle`) para sorteio ponderado performático.
- Sorteios periódicos com controle de continuidade e vencedor.

---

## 🚧 Funcionalidades em desenvolvimento

- Histórico e visualização dos sorteios realizados.
- Autenticação de endpoints e dashboard para controle dos sorteios.

---

## 🧰 Tecnologias Utilizadas

- **Python 3.13+**
- **Discord.py** – Bot no Discord
- **FastAPI** – Backend assíncrono
- **OAuth2** – Autenticação com Twitch
- **Twitch API (Helix)** – Obtenção de chatters e dados
- **PostgreSQL** – Banco de dados relacional
- **Redis** – Cache (futuramente usado)
- **psycopg2 + pool** – Driver com Connection Pooling
- **dotenv** – Variáveis de ambiente
- **ngrok** – Testes locais com exposição externa
- **asyncio.to_thread** – Execução segura de chamadas bloqueantes no backend

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

1. Clone o repositório e instale as dependências:
```bash
git clone https://github.com/seu-usuario/KinoYuBot.git
cd KinoYuBot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Crie um arquivo `.env` com suas configurações:
```env
DISCORD_TOKEN=...
CLIENT_ID=...
CLIENT_SECRET=...
DB_PASSWORD=...
```

3. Execute a API:
```bash
./init_api.sh
```

4. Execute o bot:
```bash
python bot/bot.py
```

5. Use `ngrok` se precisar expor:
```bash
ngrok http 8000
```

---

## 👨‍💻 Autor

**Eduardo Coloni**  
Desenvolvedor Backend com foco em bots, APIs, servidores e sistemas assíncronos.

---

## 📝 Licença


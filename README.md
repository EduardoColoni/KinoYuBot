
# 🎮 KinoYuBot – Discord Bot Integrado à Twitch com Sorteios Automatizados

KinoYuBot é um projeto pessoal desenvolvido com o objetivo de unir tecnologias modernas como Discord, Twitch, FastAPI e PostgreSQL em um sistema completo de sorteios ao vivo, com autenticação segura via OAuth2.

Este projeto representa minhas habilidades em **integrações de APIs**, **autenticação segura**, **comunicação entre serviços**, e **estruturação de aplicações backend**.

---

## 🎯 Objetivo do Projeto

Desenvolver um bot de Discord capaz de:

- Autenticar um streamer da Twitch via OAuth2.
- Monitorar os espectadores ativos da live.
- Realizar sorteios automáticos de itens com base em lógica de probabilidade fixa.
- Enviar notificações diretamente no Discord.

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

### 🌐 Backend com FastAPI
- API assíncrona leve com rotas organizadas.
- Rota principal de callback e home.
- Pronto para expansão com novos endpoints (ex: /sorteios, /status).

---

## 🚧 Funcionalidades em desenvolvimento

### 🎁 Sorteios com base em espectadores
- Agendamento de verificação periódica (a cada minuto).
- Lógica de sorteio de itens e espectadores.
- Lista de itens predefinida (em arquivo ou banco).
- Feedback automático de sorteio no canal do Discord.

### 📡 Integração total com a API da Twitch
- Recuperação da lista de espectadores ao vivo (via API Helix ou alternativa).
- Validação e renovação de tokens expirados com `refresh_token`.

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
- **psycopg2** – Driver PostgreSQL
- **dotenv** – Variáveis de ambiente
- **ngrok** – Exposição de APIs locais para testes

---

## 📁 Estrutura de Arquivos

```
KinoYuBot/
├── bot.py              # Lógica do bot Discord
├── main.py             # Backend FastAPI (autenticação)
├── connect.py          # Conexão com PostgreSQL
├── .env                # Tokens e variáveis sensíveis
├── README.md           # Este arquivo
├── requirements.txt    # Bibliotecas utilizadas
└── .venv/              # Ambiente virtual
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

**Eduardo Henrique**  
Desenvolvedor Backend com foco em APIs, bots e integrações em tempo real.  
Tecnologias dominadas: Python, FastAPI, PostgreSQL, Discord.py, OAuth2.

---

## 📝 Licença

Este projeto está licenciado sob a MIT License.

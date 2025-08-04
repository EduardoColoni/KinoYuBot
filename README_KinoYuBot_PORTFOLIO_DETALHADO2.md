
# 🎮 KinoYuBot – Integração entre Twitch e Discord com Backend Assíncrono

KinoYuBot é um projeto pessoal desenvolvido com o objetivo de aprofundar habilidades em desenvolvimento backend, integrações em tempo real, arquitetura modular e autenticação segura. Ele conecta a plataforma de streaming Twitch com servidores Discord, possibilitando que streamers realizem sorteios automáticos entre seus espectadores durante transmissões ao vivo, com toda a lógica e persistência tratadas por uma API desenvolvida em FastAPI.

> ⚠️ Este repositório não contém o código-fonte completo. Ele foi preparado como um demonstrativo técnico das habilidades aplicadas no desenvolvimento, ideal para avaliação de recrutadores e empresas na área de backend.

---

## 🙋‍♂️ Sobre Mim

Sou **Eduardo Coloni**, desenvolvedor backend júnior em transição de carreira. Tenho experiência com automação de rotinas, infraestrutura Linux e QA, e atualmente busco oportunidades na área de backend. Este projeto surgiu da vontade de entender mais profundamente o funcionamento de sistemas reais — por isso, evitei bibliotecas prontas sempre que possível. Dois exemplos disso são a implementação manual de **autenticação OAuth2 com Twitch** e a construção de um **pool de conexões com PostgreSQL** usando `psycopg2`.

---

## 🎯 Sobre o Projeto

O KinoYuBot funciona como um sistema completo para autenticação de streamers da Twitch, verificação de espectadores ativos e execução de sorteios com base em regras personalizadas. A comunicação é feita entre três grandes componentes:

- **Bot Discord:** responsável por receber comandos e interagir com usuários.
- **API FastAPI:** orquestra a lógica de autenticação, sorteios e integrações.
- **Banco de Dados:** armazena informações seguras sobre tokens, usuários e resultados.

---

## ✅ Funcionalidades Implementadas

### 🔐 Autenticação Twitch via OAuth2
- Fluxo completo OAuth2 com obtenção e renovação automática de tokens.
- Armazenamento seguro no PostgreSQL com tratamento de expirados.
- Callback via FastAPI com integração direta ao bot.

### 🤖 Bot Discord com `discord.py`
- Comando `!iniciar` para acionar sorteios em tempo real.
- Comunicação com a API via HTTP simulando arquitetura de microserviços.
- Estrutura modular pronta para expansão com novos comandos.

### 🎁 Sorteios com base nos espectadores ativos
- Sorteio com lógica de peso por item e controle de frequência.
- Função SQL (`make_raffle`) para execução performática dentro do banco.
- Integração direta com API da Twitch para obter chatters online.

### 🌐 Backend estruturado com FastAPI
- API assíncrona com rotas desacopladas da lógica de negócio.
- Inicialização customizada com controle de `lifespan`.
- Uso consistente de services e repositórios.

### 🗃️ Banco de Dados Relacional (PostgreSQL)
- Uso de JSON, índices, subqueries e transações seguras.
- Separação de ambientes de desenvolvimento, teste e produção.
- Estrutura planejada para escalabilidade e segurança.

---

## 🧠 Habilidades Técnicas Demonstradas

| Área               | Detalhes                                                                 |
|--------------------|--------------------------------------------------------------------------|
| Backend            | FastAPI, arquitetura MVC, organização modular                            |
| Banco de Dados     | Modelagem relacional, SQL avançado, PostgreSQL, transações e índices     |
| Integrações        | OAuth2, APIs REST (Twitch), chamadas seguras                             |
| Bots               | `discord.py`, comandos assíncronos, comunicação com backend via HTTP     |
| Infraestrutura     | `.env`, ngrok, estrutura para múltiplos ambientes                        |
| Conexão DB         | Implementação manual de `psycopg2.pool.SimpleConnectionPool`             |
| Segurança          | Armazenamento seguro de tokens, separação de credenciais e ambientes     |

---

## 🧰 Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI**
- **Discord.py**
- **Twitch API (Helix)**
- **OAuth2**
- **PostgreSQL**
- **psycopg2 com Connection Pool**
- **Redis** (planejado)
- **dotenv**
- **ngrok**

---

## 📂 Estrutura do Projeto

```
KinoYuBot/
├── bot/                  # Comandos e lógica do bot Discord
├── api/                  # Backend com FastAPI
├── core/                 # Configurações e exceções globais
├── database/
│   ├── postgres/         # Pool de conexões e repositórios
│   └── redis/            # Planejado para cache e controle temporário
```

---

## 📽️ Sugestões de Demonstração

- Print ou GIF do comando `!iniciar` disparando sorteios no Discord
- Log do sorteio com resultado e retorno do backend
- Requisição real para `/get_chatters` via Twitch Helix
- Processo de autenticação OAuth2 com refresh automático

---

## 🧪 Como Testar (Resumo)

> Não incluso neste repositório, mas pensado para rodar com:
- `.env` com variáveis do Discord, Twitch e banco.
- Backend com `uvicorn`, bot com `python bot/bot.py`.
- Exposição de endpoints com `ngrok` em ambiente local.

---

## 🧭 Objetivo deste Repositório

Este repositório visa mostrar meu conhecimento prático em desenvolvimento backend, especialmente em áreas como controle de autenticação, conexão com banco, arquitetura e integração entre serviços. Ele acompanha meu currículo como prova de conhecimento aplicado e aprendizado constante.

---

## 📬 Contato

[LinkedIn](https://www.linkedin.com/in/eduardo-coloni/)  
[GitHub](https://github.com/EduardoColoni)  
Email: eduardo.r.coloni@gmail.com

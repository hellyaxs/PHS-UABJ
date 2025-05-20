# Projeto Hardware e software 

Este projeto é uma demonstração de integração com o broker MQTT Mosquitto usando Python.

## 🚀 Tecnologias

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-660066?style=for-the-badge&logo=mqtt&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

## 📋 Pré-requisitos

- Python 3.8+
- Docker
- Docker Compose

## 🔧 Instalação

### Usando Docker Compose

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/demo_mosquitto.git
cd demo_mosquitto
```

2. Execute o projeto com Docker Compose:
```bash
docker-compose up -d
```

O projeto estará disponível em:
- Aplicação: http://localhost:8000
- MQTT Broker: localhost:1883

### Desenvolvimento Local

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/demo_mosquitto.git
cd demo_mosquitto
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o projeto:
```bash
fastapi dev src/main.py
```

## 🔧 Tecnologias Utilizadas

| Componente      | Tecnologia | Descrição                                    |
|----------------|------------|----------------------------------------------|
| Aplicação      | Python     | Aplicação principal com FastAPI              |
| Broker MQTT    | Mosquitto  | Broker MQTT para comunicação em tempo real   |
| Container      | Docker     | Containerização da aplicação                 |
| Orquestração   | Docker Compose | Gerenciamento dos containers              |
| Banco de Dados | PostgreSQL | Armazenamento persistente de dados           |

---

## 📁 Estrutura do Projeto

```tree
demo_mosquitto/
├── migrations/           # Migrations do banco de dados
├── src/
│   ├── domain/           # Entidades e regras de negócio
│   ├── repository/       # Camada de acesso a dados
│   ├── services/         # Serviços e lógica de aplicação
│   ├── events/           # Handlers de eventos e mensagens MQTT
│   ├── config/           # Configurações da aplicação 
│   │     ├── database/
│   │     ├── mosquitto/
│   │     └── settings.py 
│   └── main.py           # Ponto de entrada da aplicação
├── docs/                 # Documentação adicional
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── .env.example          # Variaveis de ambiente do projeto
└── README.md
```

## 🗃️ Migrations do Banco de Dados

O projeto utiliza SQLAlchemy com Alembic para gerenciar as migrations do banco de dados. Para executar as migrations, siga os passos abaixo:

### Gerar uma nova migration

Para criar uma nova migration após alterar os modelos:

```bash
cd src && alembic revision --autogenerate -m 'descrição da migration'
```

### Aplicar as migrations

Para aplicar todas as migrations pendentes:

```bash
cd src && alembic upgrade head
```

### Reverter a última migration

Para reverter a última migration aplicada:

```bash
cd src && alembic downgrade -1
```

### Verificar status das migrations

Para verificar quais migrations foram aplicadas:

```bash
cd src && alembic current
```

### Listar histórico de migrations

Para ver o histórico completo de migrations:

```bash
cd src && alembic history
```

## 🤝 Como Contribuir

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit das suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Padrões de Código

- Siga o guia de estilo PEP 8 para Python
- Mantenha os testes atualizados
- Documente novas funcionalidades
- Use mensagens de commit descritivas

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
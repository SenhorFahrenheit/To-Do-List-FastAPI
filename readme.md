# 🧠 Task Manager API

Uma API de gerenciamento de tarefas desenvolvida com **FastAPI**, utilizando **JWT** para autenticação e **bcrypt** para criptografia de senhas. O projeto foi criado com o objetivo de consolidar conhecimentos em backend, segurança, integração com banco de dados e estruturação de servidores.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI** - Framework web moderno e performático
- **SQLModel** - ORM baseado em SQLAlchemy e Pydantic
- **JWT (JSON Web Token)** - Autenticação segura
- **Bcrypt** - Criptografia de senhas
- **SQLite** - Banco de dados leve e eficiente (pode ser substituído por outros)
- **Uvicorn** - Servidor ASGI

---

## 🔐 Autenticação

A autenticação é feita via **JWT**. Para acessar as rotas protegidas, o usuário deve estar autenticado e enviar o token no cabeçalho da requisição (Authorization: Bearer `<seu_token>`).

---

## 📦 Funcionalidades da API

### ✅ Tarefas
- **Criar tarefa**  
  `POST /add_task`
- **Listar tarefas**  
  `GET /list_tasks`
- **Atualizar tarefa**  
  `PUT /tasks/{task_id}`
- **Remover tarefa**  
  `DELETE /tasks/{task_id}`

### 👤 Usuário
- **Cadastro**  
  `POST /sign_up` - Cria um novo usuário com e-mail e senha criptografada
- **Login**  
  `POST /sign_in` - Retorna o token JWT ao validar as credenciais

---

## 📂 Organização do Projeto

```
.
├── app/
│   ├── main.py              # Inicializa a aplicação
│   ├── routes/
│   │   ├── task.py          # Rotas relacionadas a tarefas
│   │   └── user.py          # Rotas de login e cadastro
│   ├── database/
│   │   ├── database.py      # Conexão com banco
│   │   └── model.py         # Modelos de dados
│   └── utils/
│       └── auth.py         # Funções de autenticação e criptografia
        └── functions.py
```

---

## 🥮 Como Rodar o Projeto

### 1. Clone o repositório
```bash
git clone https://github.com/SenhorFahrenheit/To-Do-List-FastAPI
cd task-api
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Inicie o servidor
```bash
uvicorn main:app --reload
```

---

## 📩 Testando a API

Acesse a documentação interativa no Swagger em:
```
http://localhost:8000/docs
```

Recomenda-se o uso do [Insomnia](https://insomnia.rest/) ou [Postman](https://www.postman.com/) para testes personalizados.

---

## 🤓 Sobre o Projeto

Este projeto foi desenvolvido com foco em aprendizado e consolidação de habilidades em:

- Design e organização de uma API RESTful
- Segurança com autenticação JWT e criptografia de senhas
- Integração com banco de dados
- Boas práticas de backend com FastAPI

---



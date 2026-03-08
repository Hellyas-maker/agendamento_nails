# 💅 Agendamento Nails

Sistema web para **agendamento de horários em salão de unhas**, desenvolvido com Python e Streamlit.

O projeto permite que clientes agendem horários online e que o administrador gerencie os agendamentos em um painel administrativo.

---

## 🚀 Tecnologias utilizadas

- Python
- Streamlit
- PostgreSQL
- Git
- GitHub

---

## 📂 Estrutura do projeto
```text
agendamento_nails
│
├── backend
│ ├── agendamentos.py
│ └── database.py
│
├── frontend
│ ├── Home.py
│ └── pages
│ ├── 1_Agendamentos.py
│ └── 2_Administrativo.py
│
├── assets
│ └── logo.png
│
├── database
│ └── create_tables.sql
│
├── requirements.txt
└── README.md
```
---

## ✨ Funcionalidades

### 👩‍💻 Área do Cliente

- Agendar horário
- Escolher data e horário
- Registrar nome e telefone

### 🔐 Área Administrativa

- Login com senha
- Visualizar agendamentos
- Cancelar agendamentos

---

## 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/Hellyas-maker/agendamento_nails.git
```
Entre na pasta:
```bash
cd agendamento_nails
```
Crie o ambiente virtual:
```bash
python -m venv venv
```
Ative o ambiente:

Windows:
```bash
venv\Scripts\activate
```
Instale as dependências:
```bash
pip install -r requirements.txt
```
---

## ▶️ Executando o projeto

Execute o Streamlit:
```bash
streamlit run frontend/Home.py
```
O sistema abrirá automaticamente no navegador.

---

## 🔐 Configuração de senha administrativa

Crie o arquivo:
```bash
.streamlit/secrets.toml
```
Adicione a senha:
```text
ADMIN_PASSWORD="sua_senha"
```
---

## 🌐 Deploy

Este projeto pode ser publicado facilmente no:

- Streamlit Cloud

Basta conectar o repositório do GitHub.

---

## 📌 Melhorias futuras

Calendário visual de agendamentos

Integração com WhatsApp

Notificação automática de agendamento

Painel administrativo mais completo

Sistema de usuários

---

## 👨‍💻 Autor

Desenvolvido por Hellyas

GitHub:
https://github.com/Hellyas-maker

---

## 📄 Licença

Este projeto está sob a licença MIT.
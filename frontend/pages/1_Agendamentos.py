# Importação de bibliotecas padrão do Python
import sys
import os
from datetime import datetime

# Aqui eu adiciono o diretório raiz do projeto ao PATH do Python.
# Isso permite importar módulos da pasta "backend" mesmo estando
# executando o arquivo dentro da pasta "frontend".
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Importa o Streamlit, biblioteca usada para criar interfaces web rapidamente com Python
import streamlit as st

# Importa funções do backend responsáveis pela lógica do sistema
# criar_agendamento -> salva um agendamento no banco
# buscar_horarios_ocupados -> consulta no banco os horários já agendados
from backend.agendamentos import criar_agendamento, buscar_horarios_ocupados

# mostrar mensagem depois do rerun
if "agendado" in st.session_state:
    st.success("✅ Agendamento realizado!")
    del st.session_state["agendado"]


# Título principal da página
st.title("Aline Lustoza - Nail Designer")

# Texto explicativo
st.write("Agende seu horário")

from datetime import timedelta

# gerar lista de domingos (próximos 365 dias)
hoje = datetime.today().date()

domingos = [
    hoje + timedelta(days=i)
    for i in range(365)
    if (hoje + timedelta(days=i)).weekday() == 6
]


# Campo de seleção de data com calendário
# Esse campo fica fora do form para permitir atualização dinâmica da página
from datetime import date
data = st.date_input("Data do agendamento", min_value=date.today(), format="DD/MM/YYYY")

if data < date.today():
    st.error("Não é possível agendar em datas passadas.")
    st.stop()

# verifica se é domingo
if data.weekday() == 6:
    st.warning("⚠️ Não atendemos aos domingos. Escolha outra data.")
    st.stop()


# Busca no banco de dados os horários já ocupados para a data escolhida
horarios_ocupados = buscar_horarios_ocupados(data)


# Converte os horários retornados do banco para string no formato HH:MM
# Exemplo: 08:00:00 -> 08:00
horarios_ocupados = [h.strftime("%H:%M") for h in horarios_ocupados]


# Lista fixa com todos os horários possíveis de atendimento
horarios_disponiveis = [
    "08:00","09:30","11:00", "12:30",
    "14:00","15:30", "17:00","18:30"]


# Pega data e hora atual
agora = datetime.now()
data_hoje = agora.date()
hora_atual = agora.strftime("%H:%M")


# Remove horários já ocupados
horarios_livres = [h for h in horarios_disponiveis if h not in horarios_ocupados]


# Impede agendamento em horários que já passaram no dia atual
if data == data_hoje:
    horarios_livres = [h for h in horarios_livres if h > hora_atual]


# Formulário apenas para envio dos dados
with st.form("form_agendamento"):

    # Campo de entrada para o nome do cliente
    nome = st.text_input("Nome do cliente")

    # Campo de seleção para escolher o serviço desejado
    servico = st.selectbox(
        "Serviço",
        [
            "Alongamento Gel na Tips",
            "Alongamento Fibra de Vidro",
            "Alongamento Molde F1",
            "Banho de Gel",
            "Outros"
        ]
    )

    # Campo de seleção para escolher o horário
    # Mostra apenas os horários livres
    hora = st.selectbox("Horário", horarios_livres)

    # Campo para telefone do cliente
    telefone = st.text_input("Telefone")

    # Botão do formulário
    enviar = st.form_submit_button("Agendar")


# Lógica executada quando o botão é clicado
if enviar:

    # Verifica se os campos obrigatórios foram preenchidos
    if nome and servico and data and hora:

        # Chama a função do backend que grava o agendamento no banco
        criar_agendamento(nome, servico, data, hora, telefone)

        # marca que o agendamento foi feito
        st.session_state["agendado"] = True

         # limpar campos
        st.session_state["nome"] = ""
        st.session_state["telefone"] = ""

        # Recarrega a página para limpar os campos
        st.rerun()

    else:
        # Caso algum campo esteja vazio
        st.error("Preencha todos os campos.")
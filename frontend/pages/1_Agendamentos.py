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

# período bloqueado
bloqueio_inicio = date(2026, 5, 1)
bloqueio_fim = date(2026, 5, 1)

data = st.date_input("Data do agendamento", min_value=date.today(), format="DD/MM/YYYY")

# bloqueia período específico
if bloqueio_inicio <= data <= bloqueio_fim:
    st.error("⚠️ Período de feriados, procure a profissional para confirmar disponibilidade de horários para essa data.")
    st.stop()

if data < date.today():
    st.error("Não é possível agendar em datas passadas.")
    st.stop()

# verifica se é domingo
if data.weekday() == 6:
    st.warning("⚠️ Não atendemos aos domingos. Escolha outra data.")
    st.stop()

if data.weekday() in (0, 4, 5):
    st.warning("⚠️ Procure a profissional para confirmar disponibilidade de horários para essa data.")
    st.stop()


# verifica se precisa de confirmação
if data.weekday() == 0:
    status = "Pendente"
else:
    status = "Agendado"


# Busca no banco de dados os horários já ocupados para a data escolhida
horarios_ocupados = buscar_horarios_ocupados(data)


# Converte os horários retornados do banco para string no formato HH:MM
# Exemplo: 08:00:00 -> 08:00
horarios_ocupados = [h.strftime("%H:%M") for h in horarios_ocupados]


# horários padrão (dias normais)
horarios_semana = [
    "08:30","10:00","11:30", "13:00",
    "14:30","16:00", "17:30","19:00"
]

# horários específicos de sábado
horarios_sabado = ["07:00", "08:30", "10:00", "11:30"]

# define quais horários usar
if data.weekday() == 5:  # sábado
    horarios_disponiveis = horarios_sabado
else:
    horarios_disponiveis = horarios_semana


# Pega data e hora atual
agora = datetime.now()
data_hoje = agora.date()
hora_atual = agora.strftime("%H:%M")


# Remove horários já ocupados
horarios_livres = [h for h in horarios_disponiveis if h not in horarios_ocupados]


# Impede agendamento em horários que já passaram no dia atual
if data == data_hoje:
    horarios_livres = [h for h in horarios_livres if h > hora_atual]



# Campo de seleção para escolher o serviço desejado
# Serviços e valores
servicos = {
    "Alongamento Gel na Tips": 110,
    "Manutenção Gel na Tips": 90,
    "Alongamento Fibra de Vidro": 130,
    "Manutenção Fibra de Vidro": 100,
    "Alongamento Molde F1": 110,
    "Manutenção Molde F1": 90,
    "Banho de Gel": 90,
    "Esmaltação em Gel": 40,
    "Mão": 25,
    "Pé": 30,
    "Pé + Mão": 50,
    "Remoção de Gel": 40,
    "Decoração Pinterest (p/ manutenção)": 20
}

servicos_por_unha = {
    "Unha Quebrada": 5,
    "Decoração Reversa": 30,
}

# cliente pode escolher vários serviços
servicos_escolhidos = st.multiselect(
    "Escolha os serviços",
    list(servicos.keys())
)

quantidades_unhas = {}

st.write("### Serviços por unha")

for servico, valor in servicos_por_unha.items():

    qtd = st.number_input(
        f"{servico} (R$ {valor} por unha)",
        min_value=0,
        max_value=10,
        step=1,
        key=servico
    )

    if qtd > 0:
        quantidades_unhas[servico] = qtd

# mostrar valores individuais
valor_total = 0

st.write("### Resumo do atendimento")

# serviços normais
for s in servicos_escolhidos:
    valor = servicos[s]
    valor_total += valor
    st.write(f"✔ {s} - R$ {valor:.2f}")

# serviços por unha
for s, qtd in quantidades_unhas.items():
    valor = servicos_por_unha[s] * qtd
    valor_total += valor
    st.write(f"✔ {s} ({qtd} unhas) - R$ {valor:.2f}")

st.write("---")
st.success(f"💰 Total: R$ {valor_total:.2f}")

# Formulário apenas para envio dos dados
with st.form("form_agendamento"):

    # Campo de entrada para o nome do cliente
    nome = st.text_input("Nome do cliente")


    # Campo de seleção para escolher o horário
    # Mostra apenas os horários livres
    hora = st.selectbox("Horário", horarios_livres)

    # Campo para telefone do cliente
    telefone = st.text_input("Telefone")

    # Botão do formulário
    enviar = st.form_submit_button("Agendar")


# Lógica executada quando o botão é clicado
if enviar:

    if status == "Pendente":
        st.success("✅ Solicitação enviada! A profissional irá confirmar seu horário em breve.")
    else:
        st.success("✅ Agendamento realizado!")

    if nome and servicos_escolhidos and data and hora:

        # montar lista de serviços
        lista_servicos = []

        # serviços normais
        lista_servicos.extend(servicos_escolhidos)

        # serviços por unha
        for s, qtd in quantidades_unhas.items():
            lista_servicos.append(f"{s} ({qtd} unhas)")

        # transformar em texto
        servicos_texto = ", ".join(lista_servicos)

        criar_agendamento(
            nome,
            servicos_texto,
            valor_total,
            data,
            hora,
            telefone,
            status
        )

        st.session_state["agendado"] = True
        st.rerun()

    if "agendado" in st.session_state:
        st.success("✅ Agendamento realizado!")
        del st.session_state["agendado"]

    else:
        st.error("Preencha todos os campos.")
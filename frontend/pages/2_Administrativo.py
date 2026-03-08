import streamlit as st
import sys
import os
from datetime import date

# Permite importar backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from backend.agendamentos import listar_agendamentos, cancelar_agendamento

senha_correta = st.secrets["ADMIN_PASSWORD"]

st.title("Painel Administrativo")

senha = st.text_input("Digite a senha", type="password")

if senha == senha_correta:

    st.success("Acesso liberado")

    st.title("Agenda da Profissional")

    data_escolhida = st.date_input(
        "Escolha a data",
        value=date.today(),
        format="DD/MM/YYYY"
    )

    agendamentos = listar_agendamentos()

    # filtra pela data
    agenda_dia = [a for a in agendamentos if a[3] == data_escolhida]

    if agenda_dia:

        # CABEÇALHO DA TABELA
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        col1.write("**Hora**")
        col2.write("**Cliente**")
        col3.write("**Serviço**")
        col4.write("**Telefone**")
        col5.write("**Status**")
        col6.write("**Ação**")

        st.divider()

        # LINHAS DA TABELA
        for ag in agenda_dia:

            id_ag = ag[0]
            cliente = ag[1]
            servico = ag[2]
            data = ag[3]
            hora = ag[4]
            telefone = ag[5]
            status = ag[6]

            col1, col2, col3, col4, col5, col6 = st.columns(6)

            col1.write(hora.strftime("%H:%M"))
            col2.write(cliente)
            col3.write(servico)
            col4.write(telefone)
            col5.write(status)

            # botão cancelar
            if status != "Cancelado":

                if col6.button("Cancelar", key=id_ag):

                    cancelar_agendamento(id_ag)

                    st.success("Agendamento cancelado!")

                    st.rerun()

            else:

                col6.write("—")

    else:

        st.info("Nenhum atendimento nesta data.")

else:

    st.warning("Digite a senha para acessar a agenda.")

import streamlit as st
import sys
import os
from datetime import date

# adiciona a raiz do projeto ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# importa o módulo do backend
import backend.agendamentos as ag

from datetime import date

senha_correta = st.secrets["ADMIN_PASSWORD"]

st.title("Painel Administrativo")

senha = st.text_input("Digite a senha", type="password")

if senha == senha_correta:

    st.success("Acesso liberado")

     # 🔔 notificação
    notificacoes = ag.buscar_agendamentos_futuros()

    if notificacoes:
        st.info("🔔 Novos agendamentos encontrados")

        for data_not, quantidade in notificacoes:
            st.write(f"📅 {data_not.strftime('%d/%m/%Y')} - {quantidade} agendamentos")

    st.title("Agenda da Profissional")

    data_escolhida = st.date_input(
        "Escolha a data",
        min_value=date.today(),
        value=date.today(),
        format="DD/MM/YYYY"
    )

    agendamentos = ag.listar_agendamentos()

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
        for item in agenda_dia:

            id_ag = item[0]
            cliente = item[1]
            servico = item[2]
            data = item[3]
            hora = item[4]
            telefone = item[5]
            status = item[6]

            col1, col2, col3, col4, col5, col6 = st.columns(6)

            col1.write(hora.strftime("%H:%M"))
            col2.write(cliente)
            col3.write(servico)
            col4.write(telefone)
            col5.write(status)

            # botão cancelar
            if status != "Cancelado":

                if col6.button("Cancelar", key=id_ag):

                    ag.cancelar_agendamento(id_ag)

                    st.success("Agendamento cancelado!")

                    st.rerun()

            else:

                col6.write("—")

    else:

        st.info("Nenhum atendimento nesta data.")

else:

    st.warning("Digite a senha para acessar a agenda.")

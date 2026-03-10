import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import backend.agendamentos as ag

st.title("Consultar meu agendamento")

st.write("Digite seu nome para verificar seu horário agendado.")

nome = st.text_input("Nome do cliente")

if st.button("Buscar agendamento"):

    if nome:

        resultados = ag.buscar_agendamentos_cliente(nome)

        if resultados:

            st.success("Agendamentos encontrados")

            for r in resultados:

                cliente = r[0]
                servico = r[1]
                data = r[2]
                hora = r[3]
                status = r[4]

                st.write("--------")
                st.write(f"👤 Cliente: {cliente}")
                st.write(f"💅 Serviço: {servico}")
                st.write(f"📅 Data: {data.strftime('%d/%m/%Y')}")
                st.write(f"⏰ Hora: {hora.strftime('%H:%M')}")
                st.write(f"📌 Status: {status}")

        else:

            st.warning("Nenhum agendamento encontrado.")

    else:

        st.error("Digite seu nome.")
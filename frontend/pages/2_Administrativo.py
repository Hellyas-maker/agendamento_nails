
import streamlit as st
import sys
import os
from pathlib import Path
from datetime import date

# Localiza a raiz do projeto
RAIZ_PROJETO = Path(__file__).resolve().parents[2]

if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

# Importa os módulos do backend
import backend.agendamentos as ag
import backend.clientes as cl


senha_correta = st.secrets["ADMIN_PASSWORD"]

st.title("Painel Administrativo")

senha = st.text_input("Digite a senha", type="password")

if senha == senha_correta:

    st.success("Acesso liberado")

    aba_agenda, aba_clientes = st.tabs([
        "📅 Agenda da Profissional",
        "👥 Cadastro de Clientes"
    ])

    with aba_agenda:
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
        agenda_dia = [a for a in agendamentos if a[4] == data_escolhida]

        try:
            faturamento_dia = sum(item[3] for item in agenda_dia if item[7] == "Agendado")

            st.metric("💰 Faturamento do dia", f"R$ {faturamento_dia:.2f}")

        except Exception:
            st.error(f"Erro ao calcular faturamento!")

        
        if agenda_dia:

            # CABEÇALHO DA TABELA
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

            col1.write("**Hora**")
            col2.write("**Cliente**")
            col3.write("**Serviço**")
            col4.write("**Valor**")
            col5.write("**Telefone**")
            col6.write("**Status**")
            col7.write("**Confirmar**")
            col8.write("**Cancelar**")

            st.divider()


            # LINHAS DA TABELA
            for item in agenda_dia:

                id_ag = item[0]
                cliente = item[1]
                servico = item[2]
                valor = item[3]
                data = item[4]
                hora = item[5]
                telefone = item[6]
                status = item[7]

                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

                col1.write(hora.strftime("%H:%M"))
                col2.write(cliente)
                col3.write(servico)
                col4.write(f"R$ {valor:.2f}")
                col5.write(telefone)
                col6.write(status)

                # botão cancelar
                if status != "Cancelado":

                    if col8.button("❌", key=id_ag):

                        ag.cancelar_agendamento(id_ag)

                        st.success("Agendamento cancelado!")

                        st.rerun()

                else:

                    col8.write("—")
                
                # botão confirmar
                if status == "Pendente":

                    if col7.button("✅", key=f"conf_{id_ag}"):

                        ag.confirmar_agendamento(id_ag)

                        st.success("Agendamento confirmado!")

                        st.rerun()

                else:
                    col7.write("—")

        else:

            st.info("Nenhum atendimento nesta data.")

    with aba_clientes:
        st.title("👥 Cadastro de Clientes")
        st.write("Gerenciamento de clientes do salão")

        aba_cadastro, aba_consulta = st.tabs([
            "➕ Novo Cliente",
            "📋 Clientes Cadastrados"
        ])


        # =====================================
        # ABA 1 - CADASTRO
        # =====================================

        with aba_cadastro:

            st.subheader("Cadastrar novo cliente")

            with st.form("form_cliente"):

                nome = st.text_input("Nome completo *")

                telefone = st.text_input(
                    "Telefone / WhatsApp *",
                    placeholder="22999999999"
                )

                email = st.text_input("E-mail")

                data_nascimento = st.date_input(
                    "Data de nascimento",
                    value=None,
                    min_value=date(1900, 1, 1)
                )

                observacoes = st.text_area("Observações")

                salvar = st.form_submit_button(
                    "Salvar cliente",
                    use_container_width=True
                )

                if salvar:

                    if not nome.strip() or not telefone.strip():

                        st.warning("Preencha nome e telefone.")

                    else:

                        cliente_id = cl.criar_cliente(
                            nome=nome.strip(),
                            telefone=telefone.strip(),
                            email=email.strip() or None,
                            data_nascimento=data_nascimento,
                            observacoes=observacoes.strip() or None
                        )

                        if cliente_id:

                            st.success(
                                f"Cliente cadastrado com sucesso! ID: {cliente_id}"
                            )

                        else:

                            st.error(
                                "Este telefone já está cadastrado."
                            )


        # =====================================
        # ABA 2 - CONSULTA
        # =====================================

        with aba_consulta:

            st.subheader("Clientes cadastrados")

            termo = st.text_input(
                "Pesquisar cliente",
                placeholder="Digite nome ou telefone"
            )

            if termo.strip():

                clientes = cl.pesquisar_clientes(termo.strip())

            else:

                clientes = cl.listar_clientes()

            if clientes:

                st.write(f"Total de registros encontrados: {len(clientes)}")

                for cliente in clientes:

                    (
                        id_cliente,
                        nome,
                        telefone,
                        email,
                        nascimento,
                        observacoes,
                        criado_em
                    ) = cliente

                    with st.expander(f"👤 {nome} - {telefone}"):

                        with st.form(f"editar_{id_cliente}"):

                            novo_nome = st.text_input(
                                "Nome",
                                value=nome
                            )

                            novo_telefone = st.text_input(
                                "Telefone",
                                value=telefone
                            )

                            novo_email = st.text_input(
                                "E-mail",
                                value=email or ""
                            )

                            novo_nascimento = st.date_input(
                                "Data de nascimento",
                                value=nascimento,
                                min_value=date(1900, 1, 1),
                                key=f"nascimento_{id_cliente}"
                            )

                            novas_observacoes = st.text_area(
                                "Observações",
                                value=observacoes or ""
                            )

                            atualizar = st.form_submit_button(
                                "Salvar alterações",
                                use_container_width=True
                            )

                            if atualizar:

                                if not novo_nome.strip() or not novo_telefone.strip():

                                    st.warning("Nome e telefone são obrigatórios.")

                                else:

                                    resultado = cl.atualizar_cliente(
                                        id_cliente=id_cliente,
                                        nome=novo_nome.strip(),
                                        telefone=novo_telefone.strip(),
                                        email=novo_email.strip() or None,
                                        data_nascimento=novo_nascimento,
                                        observacoes=novas_observacoes.strip() or None
                                    )

                                    if resultado:

                                        st.success("Cadastro atualizado!")
                                        st.rerun()

                                    else:

                                        st.error(
                                            "Não foi possível atualizar. "
                                            "Verifique se o telefone já pertence a outro cliente."
                                        )

            else:

                st.info("Nenhum cliente encontrado.")

        
else:

    st.warning("Digite a senha para acessar a agenda.")
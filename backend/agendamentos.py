# Importa a função conectar do módulo database
from datetime import date

# Importa a biblioteca psycopg2 para tratar erros do PostgreSQL
import psycopg2


# Função responsável por salvar um agendamento no banco
def criar_agendamento(cliente_nome, servico, data, hora, telefone):
    from backend.database import conectar

    # Abre conexão com o banco
    conn = conectar()

    # Cria um cursor, que é o objeto usado para executar comandos SQL
    cursor = conn.cursor()

    try:

        # Executa o comando SQL de inserção na tabela agendamentos
        cursor.execute("""
            INSERT INTO agendamentos
            (cliente_nome, servico, data_agendamento, hora_agendamento, telefone)
            VALUES (%s, %s, %s, %s, %s)
        """, (cliente_nome, servico, data, hora, telefone))

        # Confirma a transação no banco (salva os dados definitivamente)
        conn.commit()

        print("✅ Agendamento criado com sucesso!")

    # Trata erro específico do PostgreSQL quando tenta inserir horário duplicado
    except psycopg2.errors.UniqueViolation:

        # desfaz a operação
        conn.rollback()

        print("⛔ Esse horário já está ocupado!")

    finally:

        # Fecha o cursor
        cursor.close()

        # Fecha a conexão com o banco
        conn.close()


# Função responsável por consultar no banco os horários já agendados em uma data
def buscar_horarios_ocupados(data):
    from backend.database import conectar

    # Abre conexão com o banco
    conn = conectar()

    # Cria cursor para executar SQL
    cursor = conn.cursor()

    # Executa consulta que retorna os horários ocupados para a data escolhida
    cursor.execute("""
        SELECT hora_agendamento
        FROM agendamentos
        WHERE data_agendamento = %s
    """, (data,))

    # fetchall retorna todos os resultados encontrados
    resultados = cursor.fetchall()

    # fecha cursor
    cursor.close()

    # fecha conexão
    conn.close()

    # retorna apenas os horários em formato de lista
    return [r[0] for r in resultados]


# Função para listar todos os agendamentos do banco, usada na página de administração
def listar_agendamentos():
    from backend.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, cliente_nome, servico, data_agendamento, hora_agendamento, telefone, status
        FROM agendamentos
        ORDER BY data_agendamento, hora_agendamento
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


def cancelar_agendamento(id_agendamento):
    from backend.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE agendamentos
        SET status = 'Cancelado'
        WHERE id = %s
    """, (id_agendamento,))

    conn.commit()

    cursor.close()
    conn.close()


def buscar_agendamentos_futuros():
    from backend.database import conectar

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT data_agendamento, COUNT(*)
        FROM agendamentos
        WHERE data_agendamento >= CURRENT_DATE
        AND status = 'Agendado'
        GROUP BY data_agendamento
        ORDER BY data_agendamento
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados

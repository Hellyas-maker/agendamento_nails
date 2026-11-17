
# Importa a função responsável pela conexão com o banco
from backend.database import conectar

# Importa a biblioteca para tratar erros do PostgreSQL
import psycopg2


# FUNÇÃO 1: Cadastrar um novo cliente
def criar_cliente(nome, telefone, email=None,
                  data_nascimento=None, observacoes=None):

    conn = conectar()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO clientes
            (nome, telefone, email, data_nascimento, observacoes)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (nome, telefone, email, data_nascimento, observacoes))

        # Recupera o ID do cliente recém-cadastrado
        cliente_id = cursor.fetchone()[0]

        # Confirma a gravação
        conn.commit()

        return cliente_id

    except psycopg2.errors.UniqueViolation:

        # Desfaz a operação caso o telefone já exista
        conn.rollback()

        return None

    finally:
        cursor.close()
        conn.close()


# FUNÇÃO 2: Listar todos os clientes
def listar_clientes():

    conn = conectar()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT id, nome, telefone, email,
                   data_nascimento, observacoes, criado_em
            FROM clientes
            ORDER BY nome
        """)

        dados = cursor.fetchall()

        return dados

    finally:
        cursor.close()
        conn.close()


# FUNÇÃO 3: Buscar cliente pelo telefone
def buscar_cliente_telefone(telefone):

    conn = conectar()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT id, nome, telefone, email,
                   data_nascimento, observacoes
            FROM clientes
            WHERE telefone = %s
        """, (telefone,))

        cliente = cursor.fetchone()

        return cliente

    finally:
        cursor.close()
        conn.close()


# FUNÇÃO 4: Pesquisar clientes por nome ou telefone
def pesquisar_clientes(termo):

    conn = conectar()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT id, nome, telefone, email
            FROM clientes
            WHERE nome ILIKE %s
               OR telefone LIKE %s
            ORDER BY nome
        """, (f"%{termo}%", f"%{termo}%"))

        dados = cursor.fetchall()

        return dados

    finally:
        cursor.close()
        conn.close()


# FUNÇÃO 5: Atualizar cadastro de um cliente
def atualizar_cliente(id_cliente, nome, telefone,
                      email=None, data_nascimento=None,
                      observacoes=None):

    conn = conectar()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE clientes
            SET nome = %s,
                telefone = %s,
                email = %s,
                data_nascimento = %s,
                observacoes = %s
            WHERE id = %s
        """, (
            nome,
            telefone,
            email,
            data_nascimento,
            observacoes,
            id_cliente
        ))

        # Verifica se algum registro foi atualizado
        atualizado = cursor.rowcount > 0

        conn.commit()

        return atualizado

    except psycopg2.errors.UniqueViolation:

        conn.rollback()

        return False

    finally:
        cursor.close()
        conn.close()

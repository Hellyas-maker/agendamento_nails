# Importa a biblioteca responsável por conectar Python ao PostgreSQL
import psycopg2
import os
from dotenv import load_dotenv

# carrega variáveis do .env
load_dotenv()

# Função responsável por criar e retornar uma conexão com o banco de dados
def conectar():

    # psycopg2.connect abre uma conexão com o PostgreSQL usando os parâmetros abaixo
    conn = psycopg2.connect(

        # endereço do servidor do banco (localhost = seu próprio computador)
        host=os.getenv("DB_HOST"),

        # nome do banco de dados que criamos
        database=os.getenv("DB_NAME"),

        # usuário do PostgreSQL
        user=os.getenv("DB_USER"),

        # senha do banco
        password=os.getenv("DB_PASSWORD"),

        # porta padrão do PostgreSQL
        port=os.getenv("DB_PORT")
    )

    # retorna o objeto de conexão para que outras partes do sistema possam usar
    return conn

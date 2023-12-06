import psycopg2
from psycopg2 import OperationalError
import time

def create_connection():
    """ Cria uma conexão com o banco de dados PostgreSQL através do HAProxy. """
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bd123",
            host="localhost",
            port="5450",
            database="master"
        )
        #print("Conexão com PostgreSQL estabelecida.")
        return connection
    except OperationalError as e:
        print(f"Erro '{e}' ao conectar ao PostgreSQL.")
        return None

def execute_query(connection, query):
    """ Executa uma consulta SQL e fecha a conexão. """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            print(f"Servidor conectado: {result}")
    except OperationalError as e:
        print(f"Erro '{e}' ao executar a consulta.")
    finally:
        connection.close()

def main():
    # Executa a consulta várias vezes para simular diferentes solicitações
    for _ in range(1000):
        connection = create_connection()
        if connection:
            execute_query(connection, "SELECT inet_server_addr(), inet_server_port();")
            time.sleep(1)  # Intervalo de 1 segundo entre as consultas

if __name__ == "__main__":
    main()

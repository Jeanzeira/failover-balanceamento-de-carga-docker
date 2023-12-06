import psycopg2
from psycopg2 import Error
from faker import Faker

fake = Faker()

def adicionar_dados(nome, idade, email):
    try:
        conexao = psycopg2.connect(
            user="postgres",
            password="bd123",
            host="localhost",
            port="5440",
            database="master"
        )

        cursor = conexao.cursor()

        comando_sql = "INSERT INTO usuarios (nome, idade, email) VALUES (%s, %s, %s)"
        valores = (nome, idade, email)

        cursor.execute(comando_sql, valores)

        conexao.commit()
        print("Dados adicionados com sucesso!")
    except (Exception, Error) as error:
        print(f"Erro ao adicionar dados: {error}")
    finally:
        if conexao:
            cursor.close()
            conexao.close()

fake = Faker()

for _ in range(10):
    nome = fake.name()
    idade = fake.random_int(min=18, max=80)
    email = fake.email()
    print(nome, idade, email)

    adicionar_dados(nome, idade, email)

    #criar tabela no postgres
    #CREATE TABLE usuarios (
    #id SERIAL PRIMARY KEY,
    #nome VARCHAR(100),
    #idade INTEGER,
    #email VARCHAR(100));
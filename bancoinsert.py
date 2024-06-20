import psycopg2
from psycopg2 import Error
from faker import Faker

fake = Faker()

def adicionar_endereco(rua, cidade, estado, cep):
    try:
        conexao = psycopg2.connect(
            user="postgres",
            password="bd123",
            host="localhost",
            port="5440",
            database="master"
        )
        cursor = conexao.cursor()

        comando_sql = """
            INSERT INTO enderecos (rua, cidade, estado, cep)
            VALUES (%s, %s, %s, %s) RETURNING id
        """
        valores = (rua, cidade, estado, cep)

        cursor.execute(comando_sql, valores)
        endereco_id = cursor.fetchone()[0]

        conexao.commit()
        return endereco_id
    except (Exception, Error) as error:
        print(f"Erro ao adicionar endereço: {error}")
        return None
    finally:
        if conexao:
            cursor.close()
            conexao.close()

def adicionar_usuario(nome, idade, email, telefone, endereco_id):
    try:
        conexao = psycopg2.connect(
            user="postgres",
            password="bd123",
            host="localhost",
            port="5440",
            database="master"
        )
        cursor = conexao.cursor()

        comando_sql = """
            INSERT INTO usuarios (nome, idade, email, telefone, endereco_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nome, idade, email, telefone, endereco_id)

        cursor.execute(comando_sql, valores)

        conexao.commit()
        print("Dados do usuário adicionados com sucesso!")
    except (Exception, Error) as error:
        print(f"Erro ao adicionar dados do usuário: {error}")
    finally:
        if conexao:
            cursor.close()
            conexao.close()

# Gerar e adicionar dados de exemplo
for _ in range(10000):  # Ajustado inserções para teste
    nome = fake.name()
    idade = fake.random_int(min=18, max=80)
    email = fake.email()
    telefone = fake.phone_number()[:15]  # Truncar telefone para no máximo 15 caracteres
    rua = fake.street_address()
    cidade = fake.city()
    estado = fake.state()
    cep = fake.postcode()

    endereco_id = adicionar_endereco(rua, cidade, estado, cep)

    if endereco_id:
        adicionar_usuario(nome, idade, email, telefone, endereco_id)

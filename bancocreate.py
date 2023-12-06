import psycopg2

try:
    # Conectar ao banco de dados PostgreSQL usando o context manager
    with psycopg2.connect(
        user="postgres",
        password="bd123",
        host="localhost",
        port="5440",
        database="master"
    ) as conn:

        # Abrir um cursor para executar comandos SQL
        with conn.cursor() as cur:

            # Comando SQL para criar uma tabela
            query = """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100),
                    idade INTEGER,
                    email VARCHAR(100)
                )
            """

            # Executar o comando SQL
            cur.execute(query)

            # Commit da transação para efetivar a criação da tabela
            conn.commit()

        print("Tabela criada com sucesso!")

except (psycopg2.Error, psycopg2.DatabaseError) as e:
    print("Erro ao criar a tabela 'usuarios':", e)

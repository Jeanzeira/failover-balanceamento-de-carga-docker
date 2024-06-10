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

            # Comando SQL para criar a tabela usuarios
            query_usuarios = """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    idade INTEGER CHECK (idade > 0),
                    email VARCHAR(100) UNIQUE NOT NULL,
                    telefone VARCHAR(15),
                    endereco_id INTEGER,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'ativo',
                    CONSTRAINT fk_endereco
                        FOREIGN KEY(endereco_id) 
                            REFERENCES enderecos(id)
                            ON DELETE SET NULL
                )
            """

            # Comando SQL para criar a tabela enderecos
            query_enderecos = """
                CREATE TABLE IF NOT EXISTS enderecos (
                    id SERIAL PRIMARY KEY,
                    rua VARCHAR(100) NOT NULL,
                    cidade VARCHAR(50) NOT NULL,
                    estado VARCHAR(50) NOT NULL,
                    cep VARCHAR(10) NOT NULL
                )
            """

            # Executar os comandos SQL
            cur.execute(query_enderecos)
            cur.execute(query_usuarios)

            # Commit da transação para efetivar a criação das tabelas
            conn.commit()

        print("Tabelas criadas com sucesso!")

except (psycopg2.Error, psycopg2.DatabaseError) as e:
    print("Erro ao criar as tabelas:", e)

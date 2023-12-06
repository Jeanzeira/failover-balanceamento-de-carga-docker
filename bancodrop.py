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

            # Comando SQL para excluir a tabela se ela existir
            drop_query = "DROP TABLE IF EXISTS usuarios CASCADE"

            # Executar o comando SQL
            cur.execute(drop_query)

            # Commit da transação para efetivar a exclusão da tabela
            conn.commit()

        print("Tabela 'usuarios' excluída com sucesso!")

except (psycopg2.Error, psycopg2.DatabaseError) as e:
    print("Erro ao excluir a tabela 'usuarios':", e)

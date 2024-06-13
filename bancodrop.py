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

            # Comando SQL para excluir a tabela 'usuarios' se ela existir
            drop_usuarios_query = "DROP TABLE IF EXISTS usuarios CASCADE"
            cur.execute(drop_usuarios_query)

            # Comando SQL para excluir a tabela 'enderecos' se ela existir
            drop_enderecos_query = "DROP TABLE IF EXISTS enderecos CASCADE"
            cur.execute(drop_enderecos_query)

            # Commit da transação para efetivar a exclusão das tabelas
            conn.commit()

        print("Tabelas 'usuarios' e 'enderecos' excluídas com sucesso!")

except (psycopg2.Error, psycopg2.DatabaseError) as e:
    print("Erro ao excluir as tabelas 'usuarios' e 'enderecos':", e)

import psycopg2

try:
    # Conectar ao banco de dados PostgreSQL
    conn = psycopg2.connect(
        user="postgres",
        password="bd123",
        host="localhost",
        port="5440",
        database="master"
    )

    # Abrir um cursor para executar comandos SQL
    cur = conn.cursor()

    # Comando SQL para atualizar dados na tabela
    query = "UPDATE usuarios SET idade = 10 WHERE idade <=50;"

    # Executar o comando SQL
    cur.execute(query)

    # Commit da transação para efetivar a atualização
    conn.commit()

    print("Atualização realizada com sucesso!")

except psycopg2.Error as e:
    print("Erro ao atualizar os dados:", e)

finally:
    # Fechar o cursor e a conexão com o banco de dados
    if cur:
        cur.close()
    if conn:
        conn.close()

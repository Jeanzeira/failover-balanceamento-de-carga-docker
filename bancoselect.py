import psycopg2

# Conectar ao banco de dados PostgreSQL
conn = psycopg2.connect(
    user="postgres",
    password="bd123",
    host="localhost",
    port="5450",
    database="master"
)

# Abrir um cursor para executar comandos SQL
cur = conn.cursor()

# Comando SQL com o subselect para unir os resultados
query = """
    SELECT *,
        (SELECT inet_server_addr()) AS server_address,
        (SELECT inet_server_port()) AS server_port
        FROM usuarios
        ORDER BY id asc;
"""


# Executar o comando SQL
cur.execute(query)

# Recuperar os resultados
rows = cur.fetchall()

# Mostrar os resultados
for row in rows:
    print(row)

# Fechar o cursor e a conexão com o banco de dados
cur.close()
conn.close()

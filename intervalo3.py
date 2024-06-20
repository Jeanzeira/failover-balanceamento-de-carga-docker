import psycopg2
import time

def get_partitioned_select(id_start, id_end):
    return f"""
        SELECT u.id, u.nome, u.idade, u.email, u.telefone,
               e.rua, e.cidade, e.estado, e.cep,
               TO_CHAR(u.data_criacao, 'DD-MM-YYYY HH24:MI:SS') AS data_criacao_formatada,
               (SELECT COUNT(*) FROM usuarios) AS total_usuarios,
               (SELECT inet_server_addr()) AS server_address,
               (SELECT inet_server_port()) AS server_port
        FROM usuarios u
        INNER JOIN enderecos e ON u.endereco_id = e.id
        WHERE u.id BETWEEN {id_start} AND {id_end}
        ORDER BY u.id ASC;
    """

def execute_query():
    server = {"host": "localhost", "port": 5442, "dbname": "master", "user": "postgres", "password": "bd123"}
    conn = None
    start_time = time.time()
    try:
        conn = psycopg2.connect(
            host=server['host'],
            port=server['port'],
            dbname=server['dbname'],
            user=server['user'],
            password=server['password']
        )
        cursor = conn.cursor()
        cursor.execute(get_partitioned_select(318933, 478398))
        rows = cursor.fetchall()
        formatted_rows = "\n".join([str(row) for row in rows])
        print(f"Resultado da requisição no servidor {server['host']}:{server['port']}:\n{formatted_rows}")
    except Exception as e:
        print(f"Erro ao processar a requisição no servidor {server['host']}:{server['port']}: {e}")
    finally:
        if conn:
            conn.close()
        end_time = time.time()
        print(f"Tempo de execução para o intervalo de IDs 318933 a 478398: {end_time - start_time} segundos")

execute_query()

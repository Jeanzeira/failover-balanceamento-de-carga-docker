import psycopg2
import time
import multiprocessing

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

def execute_query(id_start, id_end, port):
    server = {"host": "localhost", "port": port, "dbname": "master", "user": "postgres", "password": "bd123"}
    conn = None
    try:
        conn = psycopg2.connect(
            host=server['host'],
            port=server['port'],
            dbname=server['dbname'],
            user=server['user'],
            password=server['password']
        )
        cursor = conn.cursor()
        cursor.execute(get_partitioned_select(id_start, id_end))
        rows = cursor.fetchall()
        formatted_rows = "\n".join([str(row) for row in rows])
        print(f"Resultado da requisição no servidor {server['host']}:{server['port']}:\n{formatted_rows}\n")
    except Exception as e:
        print(f"Erro ao processar a requisição no servidor {server['host']}:{server['port']}: {e}\n")
    finally:
        if conn:
            conn.close()

def execute_queries_serial():
    intervals = [(1, 1000000), (1000001, 2000000)]
    port = 5440
    start_time = time.time()
    for id_start, id_end in intervals:
        execute_query(id_start, id_end, port)
    end_time = time.time()
    print(f"Tempo de execução serial: {end_time - start_time} segundos\n")

def execute_queries_parallel():
    intervals = [(1, 1000000), (1000001, 2000000)]
    ports = [5440, 5441]
    start_time = time.time()
    processes = []
    for (id_start, id_end), port in zip(intervals, ports):
        p = multiprocessing.Process(target=execute_query, args=(id_start, id_end, port))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    end_time = time.time()
    print(f"Tempo de execução paralelo: {end_time - start_time} segundos\n")

if __name__ == '__main__':
    # Serial
    execute_queries_serial()
    
    # Pausa de 5 segundos
    time.sleep(5)
    
    # Paralelo
    execute_queries_parallel()

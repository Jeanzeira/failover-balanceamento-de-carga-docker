import threading
import queue
import random
import time
import psycopg2

class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.request_queue = queue.Queue()
        self.current_server = 0
        self.lock = threading.Lock()
        
    def get_next_server(self):
        with self.lock:
            server = self.servers[self.current_server]
            self.current_server = (self.current_server + 1) % len(self.servers)
        return server

    def handle_request(self, request):
        server = self.get_next_server()
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
            cursor.execute(request)
            rows = cursor.fetchall()
            print(f"Resultado da requisição no servidor {server['host']}:{server['port']}: {rows}")
        except Exception as e:
            print(f"Erro ao processar a requisição no servidor {server['host']}:{server['port']}: {e}")
        finally:
            if conn:
                conn.close()

    def start(self):
        while True:
            request = self.request_queue.get()
            if request is None:
                break
            self.handle_request(request)

    def add_request(self, request):
        self.request_queue.put(request)

# Função que retorna o SELECT complexo
def get_complex_select():
    return """
        SELECT u.id, u.nome, u.idade, u.email, u.telefone,
               e.rua, e.cidade, e.estado, e.cep,
               TO_CHAR(u.data_criacao, 'DD-MM-YYYY HH24:MI:SS') AS data_criacao_formatada,
               (SELECT COUNT(*) FROM usuarios) AS total_usuarios,
               (SELECT inet_server_addr()) AS server_address,
               (SELECT inet_server_port()) AS server_port
        FROM usuarios u
        INNER JOIN enderecos e ON u.endereco_id = e.id
        ORDER BY u.id ASC;
    """

# Definir a lista de servidores
servers = [
    {"host": "localhost", "port": 5440, "dbname": "master", "user": "postgres", "password": "bd123"},  # Master
    {"host": "localhost", "port": 5441, "dbname": "master", "user": "postgres", "password": "bd123"},  # Slave 0
    {"host": "localhost", "port": 5442, "dbname": "master", "user": "postgres", "password": "bd123"},  # Slave 1
    {"host": "localhost", "port": 5443, "dbname": "master", "user": "postgres", "password": "bd123"}   # Slave 2
]

# Criar e iniciar o balanceador de carga
load_balancer = LoadBalancer(servers)
threading.Thread(target=load_balancer.start).start()

# Simular a adição de requisições de SELECT
for i in range(10):
    load_balancer.add_request(get_complex_select())
    time.sleep(random.uniform(0.1, 1.0))

# Enviar um sinal de parada
load_balancer.add_request(None)

import redis


class RedisAdapter:
    def __init__(self):
        self.conexao = redis.Redis(host='redis-service', port=6379)

    def enfileirar(self, fila, mensagem):
        if self.conexao is not None:
            self.conexao.lpush(fila, mensagem)

    def verificar_conexao(self):
        return self.conexao.ping()

    def fechar_conexao(self):
        if self.conexao is not None:
            self.conexao.close()
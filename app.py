import json
import time
from flask import Flask, request, jsonify, make_response, Response
from prometheus_client import Counter, generate_latest, Histogram
from src.application.factory.LoggerFactory import LoggerFactory
from src.infra.RedisAdapter import RedisAdapter

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024

logger = LoggerFactory.create_logger('imagens', 'logs/imagens.log', terminal=False)
REQUEST_COUNT = Counter('request_count', 'Contagem de solicitações', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Latência das solicitações', ['method', 'endpoint'])
redis = RedisAdapter()


@app.before_request
def before_request():
    request.start_time = time.time()


@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.method, request.path).observe(latency)
    return response


def mostrar_dados_requisicao(request):
    conteudo_request = ""

    for chave, valor in request.form.items():
        if chave != 'img':
            conteudo_request += f'({chave}: {valor}) - '

    logger.error(f'{request} - Conteúdo inválido: {conteudo_request}')


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype="text/plain")


@app.route('/baixas/status')
def status():
    try:
        if redis.verificar_conexao():
            status = 'OK'
        else:
            status = "Conexão Perdida"

    except Exception as erro:
        status = f"Erro ao conectar ao banco: {erro}"

    return jsonify({"status": status})


@app.route('/baixas/', methods=['GET', 'POST'])
def baixas():
    try:
        if request.form.get('idr') is None or request.form.get('chaveCTE') is None:
            mostrar_dados_requisicao(request)
            response = jsonify({'error': 'chave inválida'})
            return make_response(response, 500)

        chave_acesso = request.form.get('idr')
        logger.info(f"chave_acesso - {chave_acesso}")

        if not redis.conexao:
            mensagem = 'redis nao conectado'
            logger.warning(mensagem)
            response = jsonify({'error': mensagem})
            return make_response(response, 408)

        formulario = json.dumps(request.form)
        redis.enfileirar('imagens', formulario)
        logger.info(f"integrando - {request.form.get('chaveCTE')}")

        response = jsonify({'result': f"integrado {request.form.get('chaveCTE')}"})
        return make_response(response, 200)

    except Exception as error:
        logger.critical(f"Ocorreu um erro ao processar requisição: {error}")
        response = jsonify({'error': str(error)})
        return make_response(response, 408)


if __name__ == "__main__":
    app.run()

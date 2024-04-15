FROM python:3.11-alpine

# Definir o Python como UNBUFFERED
ENV PYTHONUNBUFFERED=1

# Criando o diretório de trabalho
WORKDIR /app

# Criar o diretório de logs e adicionar um arquivo de log inicial
RUN mkdir -p /app/logs && touch /app/logs/imagens.log

# Copiar arquivo de requirements.txt
COPY requirements.txt ./

COPY . /app

RUN ls -la /app
# Instalando as bibliotecas necessárias para aplicação
RUN pip install --no-cache-dir -r requirements.txt


#SET FLASK_APP=app

# Expor a porta em que a aplicação Gunicorn irá rodar
EXPOSE 8004

# Comando executado ao iniciar o container
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8004"]

# Criar a rede necessária para o Redis
# docker network create redis-network

# Subir o Redis (Caso ainda não exista)
# docker run --network redis-network -d --name redis-container -p 6379:6379 redis:7.2.4-alpine

# Sugestão de comando para criar a imagem
# docker build --tag luizfelipekraus/api-imagens-image .

# Sugestão de comando para criar o container
# docker run -p 8004:8004 --network redis-network --name api-imagens-container -v ${PWD}:/app -d luizfelipekraus/api-imagens-image

# Sugestão de comando para acessar o container
# docker exec -it luizfelipekraus/api-imagens-container /bin/sh


#subir para dockerhub
#git push api-imagens-container

#grafana
#docker run --name dashboards -d -p 3000:3000 --net=redis-network grafana/grafana-enterprise

#phometeus
#docker run  --name prometheus-container -d -p 9090:9090 --network redis-network -v ${PWD}/prometheus.yaml:/etc/prometheus/prometheus.yml  prom/prometheus

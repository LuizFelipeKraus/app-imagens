pipeline {
    agent {
        label 'my-local-agent'
    }

    stages {
        stage('Build') {
            steps {
                script {
                    // Clonar o repositório Git
                    sh 'git clone https://github.com/LuizFelipeKraus/app-imagens.git'
                    // Build da imagem Docker
                    sh 'docker build -t luizfelipekraus/api-imagens-image .'
                }
            }
        }
        stage('Deploy') {
            steps {
                // Aplicar o arquivo de serviço Kubernetes
                sh 'kubectl apply -f app-service.yaml'
            }
        }
    }
}

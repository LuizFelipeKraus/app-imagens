pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t luizfelipekraus/api-imagens-image .'
            }
        }
        stage('Test') {
            steps {

            }
        }
        stage('Deploy') {
            steps {
                sh 'kubectl apply -f app-deployment.yaml'
            }
        }
    }
}

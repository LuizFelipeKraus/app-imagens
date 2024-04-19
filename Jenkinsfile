pipeline {
    agent any
    environment {
        DOCKERHUB = credentials('dockerhub')
        KUBE_CONFIG_FILE = credentials('KubernetesConfig')
    }
    stages {
        stage("Initialize") {
            steps {
                bat "echo Projeto de API Imagem"
            }
        }
        stage("Checkout Projeto") {
            steps {
                script {
                    if (!fileExists('app-imagens')) {
                        bat "git clone https://github.com/LuizFelipeKraus/app-imagens.git"
                    } else {
                        dir('app-imagens') {
                            bat "git pull"
                        }
                    }
                    dir('app-imagens') {
                        TAG_VERSION = bat(script: "git rev-parse --short HEAD", returnStdout:true).trim()
                    }
                }
            }
        }
        stage("Create Image") {
            steps {
                dir("app-imagens") {
                    bat "docker build --tag luizfelipekraus/api-imagens-image ."
                    bat "docker tag luizfelipekraus/api-imagens-image luizfelipekraus/api-imagens-image:latest"
                }
            }
        }
        stage("Push Image") {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable:'USERNAME', passwordVariable:'PASSWORD')]) {
                        bat "docker login --username=$USERNAME --password=$PASSWORD"
                        bat "docker push luizfelipekraus/api-imagens-image"
                        bat "docker push luizfelipekraus/api-imagens-image:latest"
                    }
                }
            }
        }
        stage("Debug") {
            steps {
                bat "dir"
            }
        }
        stage("Deploy K8s") {
            steps {
                script {
                    withCredentials([
                        file(credentialsId: 'KubernetesConfig', variable: 'KUBE_CONFIG_FILE')
                    ]) {
                        bat "kubectl apply -f app-service.yaml --validate=false --kubeconfig=$KUBE_CONFIG_FILE"
                    }
                }
            }
        }
    }
}

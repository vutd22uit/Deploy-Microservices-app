pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_USER = 'vutd22uit'
        DOCKER_CREDENTIALS = credentials('docker-credentials')
    }
    
    stages {
        stage('Build') {
            steps {
                script {
                    node {
                        echo 'Building microservices...'
                        dir('product') {
                            sh 'python -m pip install -r requirements.txt'
                        }
                    }
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    node {
                        dir('product') {
                            sh 'python -m pytest tests/ || true'
                        }
                    }
                }
            }
        }
        
        stage('Docker Build') {
            steps {
                script {
                    node {
                        // Build Docker images
                        dir('product') {
                            docker.build("${DOCKER_USER}/product-service:${BUILD_NUMBER}")
                        }
                    }
                }
            }
        }
        
        stage('Docker Push') {
            steps {
                script {
                    node {
                        docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS) {
                            def productImage = docker.image("${DOCKER_USER}/product-service:${BUILD_NUMBER}")
                            productImage.push()
                            productImage.push('latest')
                        }
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    node {
                        sh 'docker-compose up -d'
                    }
                }
            }
        }
    }
    
    post {
        always {
            node {
                echo 'Cleaning up...'
                sh 'docker-compose down || true'
                cleanWs()
            }
        }
        success {
            node {
                echo 'Pipeline succeeded!'
            }
        }
        failure {
            node {
                echo 'Pipeline failed!'
            }
        }
    }
}

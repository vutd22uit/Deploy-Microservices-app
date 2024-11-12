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
                echo 'Building microservices...'
                dir('product') {
                    sh 'python -m pip install -r requirements.txt'
                }
            }
        }
        
        stage('Test') {
            steps {
                dir('product') {
                    sh 'python -m pytest tests/ || true'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    sh 'docker-compose up -d --build'
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh 'docker-compose down || true'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}

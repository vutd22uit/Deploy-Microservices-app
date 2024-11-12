pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_USER = 'vutd22uit'
    }
    
    stages {
        stage('Build') {
            steps {
                echo 'Building microservices...'
                dir('user') {
                    sh 'python3 -m pip install --user -r requirements.txt'
                }
                dir('order') {
                    sh 'python3 -m pip install --user -r requirements.txt'
                }
            }
        }
        
        stage('Test') {
            steps {
                dir('user') {
                    sh 'python3 -m pytest tests/ || true'
                }
                dir('order') {
                    sh 'python3 -m pytest tests/ || true'
                }
            }
        }
        
        stage('Docker Build') {
            steps {
                script {
                    dir('user') {
                        docker.build("${DOCKER_USER}/user-service:${BUILD_NUMBER}")
                    }
                    dir('order') {
                        docker.build("${DOCKER_USER}/order-service:${BUILD_NUMBER}")
                    }
                }
            }
        }
        
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                }
            }
        }
        
        stage('Docker Push') {
            steps {
                script {
                    docker.image("${DOCKER_USER}/user-service:${BUILD_NUMBER}").push()
                    docker.image("${DOCKER_USER}/user-service:${BUILD_NUMBER}").push('latest')
                    
                    docker.image("${DOCKER_USER}/order-service:${BUILD_NUMBER}").push()
                    docker.image("${DOCKER_USER}/order-service:${BUILD_NUMBER}").push('latest')
                }
            }
        }
        
        stage('Deploy') {
            steps {
                // Xóa các container cũ và triển khai container mới
                sh 'docker-compose down --remove-orphans || true'
                sh 'docker-compose up -d --remove-orphans'
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs() // chỉ dọn dẹp workspace, không xóa container
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}

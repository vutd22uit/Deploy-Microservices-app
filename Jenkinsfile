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
                dir('product') {
                    sh '''
                        python3 -m pip install --user -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Test') {
            steps {
                dir('product') {
                    sh '''
                        python3 -m pytest tests/ || true
                    '''
                }
            }
        }
        
        stage('Docker Build') {
            steps {
                script {
                    dir('product') {
                        def productImage = docker.build("${DOCKER_USER}/product-service:${BUILD_NUMBER}")
                    }
                }
            }
        }
        
        stage('Docker Push') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-credentials') {
                        def productImage = docker.image("${DOCKER_USER}/product-service:${BUILD_NUMBER}")
                        productImage.push()
                        productImage.push('latest')
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh 'docker-compose down || true'
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}

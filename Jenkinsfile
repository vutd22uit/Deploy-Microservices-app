pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_USER = 'vutd22uit'
        PRODUCT_SERVICE = 'product-service'
        USER_SERVICE = 'user-service'
        DOCKER_CREDENTIALS = credentials('docker-credentials')
        SONAR_TOKEN = credentials('sonar-token')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            parallel {
                stage('Product Service') {
                    steps {
                        dir('product') {
                            sh '''
                                python -m venv venv
                                . venv/bin/activate
                                pip install -r requirements.txt
                            '''
                        }
                    }
                }
                
                stage('User Service') {
                    steps {
                        dir('user') {
                            sh '''
                                python -m venv venv
                                . venv/bin/activate
                                pip install -r requirements.txt
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Run Tests') {
            parallel {
                stage('Test Product Service') {
                    steps {
                        dir('product') {
                            sh '''
                                . venv/bin/activate
                                python -m pytest tests/ || true
                                python -m coverage run -m pytest tests/
                                python -m coverage report
                            '''
                        }
                    }
                }
                
                stage('Test User Service') {
                    steps {
                        dir('user') {
                            sh '''
                                . venv/bin/activate
                                python -m pytest tests/ || true
                                python -m coverage run -m pytest tests/
                                python -m coverage report
                            '''
                        }
                    }
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        # Scan product service
                        cd product
                        sonar-scanner \
                            -Dsonar.projectKey=product-service \
                            -Dsonar.sources=. \
                            -Dsonar.python.coverage.reportPaths=coverage.xml \
                            -Dsonar.host.url=http://localhost:9000
                            
                        # Scan user service
                        cd ../user
                        sonar-scanner \
                            -Dsonar.projectKey=user-service \
                            -Dsonar.sources=. \
                            -Dsonar.python.coverage.reportPaths=coverage.xml \
                            -Dsonar.host.url=http://localhost:9000
                    '''
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                script {
                    // Build Product service
                    dir('product') {
                        docker.build("${DOCKER_USER}/${PRODUCT_SERVICE}:${BUILD_NUMBER}")
                    }
                    
                    // Build User service
                    dir('user') {
                        docker.build("${DOCKER_USER}/${USER_SERVICE}:${BUILD_NUMBER}")
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                parallel(
                    "Scan Product Image": {
                        sh "trivy image ${DOCKER_USER}/${PRODUCT_SERVICE}:${BUILD_NUMBER}"
                    },
                    "Scan User Image": {
                        sh "trivy image ${DOCKER_USER}/${USER_SERVICE}:${BUILD_NUMBER}"
                    }
                )
            }
        }
        
        stage('Push Docker Images') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", DOCKER_CREDENTIALS) {
                        // Push Product service
                        docker.image("${DOCKER_USER}/${PRODUCT_SERVICE}:${BUILD_NUMBER}").push()
                        docker.image("${DOCKER_USER}/${PRODUCT_SERVICE}:${BUILD_NUMBER}").push('latest')
                        
                        // Push User service
                        docker.image("${DOCKER_USER}/${USER_SERVICE}:${BUILD_NUMBER}").push()
                        docker.image("${DOCKER_USER}/${USER_SERVICE}:${BUILD_NUMBER}").push('latest')
                    }
                }
            }
        }
        
        stage('Deploy Services') {
            steps {
                script {
                    sh """
                        docker-compose down
                        docker-compose up -d
                    """
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline execution failed!'
        }
    }
}

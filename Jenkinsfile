pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_USER = 'vutd22uit'
        PATH = "/var/lib/jenkins/.local/bin:$PATH"
    }

    stages {
        stage('Prepare Environment') {
            steps {
                sh '''
                python3 -m pip install --user --upgrade pip
                python3 -m pip install --user pytest
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Building microservices...'
                dir('user') {
                    sh '''
                    python3 -m pip install --user -r requirements.txt
                    '''
                }
                dir('order') {
                    sh '''
                    python3 -m pip install --user -r requirements.txt
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                dir('user') {
                    sh 'python3 -m pytest tests/'
                }
                dir('order') {
                    sh 'python3 -m pytest tests/'
                }
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    dir('user') {
                        sh "docker build -t ${DOCKER_USER}/user-service:${env.BUILD_NUMBER} ."
                    }
                    dir('order') {
                        sh "docker build -t ${DOCKER_USER}/order-service:${env.BUILD_NUMBER} ."
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
                    sh "docker push ${DOCKER_USER}/user-service:${env.BUILD_NUMBER}"
                    sh "docker push ${DOCKER_USER}/user-service:latest"
                    sh "docker push ${DOCKER_USER}/order-service:${env.BUILD_NUMBER}"
                    sh "docker push ${DOCKER_USER}/order-service:latest"
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose down --remove-orphans || true'
                sh 'docker-compose up -d --remove-orphans'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
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

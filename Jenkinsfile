pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_USER = 'vutd22uit'
        SONARQUBE_ENV = 'SonarQube' // Tên server SonarQube trong Jenkins
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

        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv("${SONARQUBE_ENV}") { // Tích hợp SonarQube
                        sh '''
                        sonar-scanner \
                            -Dsonar.projectKey=user-service \
                            -Dsonar.sources=user \
                            -Dsonar.host.url=$SONAR_HOST_URL \
                            -Dsonar.login=$SONAR_AUTH_TOKEN
                        '''
                        sh '''
                        sonar-scanner \
                            -Dsonar.projectKey=order-service \
                            -Dsonar.sources=order \
                            -Dsonar.host.url=$SONAR_HOST_URL \
                            -Dsonar.login=$SONAR_AUTH_TOKEN
                        '''
                    }
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
                sh '''
                docker-compose down --remove-orphans || true
                docker-compose up -d --remove-orphans
                '''
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

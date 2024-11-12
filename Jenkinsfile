pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building microservices...'
                // Chạy build cho từng service nếu cần thiết
                dir('product') {
                    // Ví dụ: chạy lệnh build Maven hoặc npm nếu project cần
                    sh 'mvn clean install'  // hoặc thay thế bằng lệnh khác nếu cần
                }
                dir('user') {
                    sh 'mvn clean install'  // hoặc thay thế bằng lệnh khác nếu cần
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Chạy test cho từng service
                dir('product') {
                    sh 'mvn test'
                }
                dir('user') {
                    sh 'mvn test'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying services using Docker Compose...'
                sh 'docker-compose up -d --build'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'docker-compose down'  // Dừng các container sau khi deploy
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}

pipeline{
    agent any

    environment{
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages{
        stage('Checkout'){
            steps{
                checkout scm
            }
        }

        stage('Tear Down'){
            steps{
                bat 'docker compose down --rmi local || true'
            }
        }

        stage('Build'){
            steps{
                bat 'docker compose build --no-cache flask-app'
            }
        }

        stage('Run'){
            steps{
                bat 'docker compose up -d'
            }
        }
    }
    post{
        success{
            echo 'Redeployed successfully'
        }
        failure{
            echo 'Pipeline failed. Check logs'
        }
    }
}


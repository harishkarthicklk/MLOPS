pipeline {

    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r backend/requirements.txt'
            }
        }

        stage('Compare Models') {
            steps {
                bat 'python backend/compare_models.py'
            }
        }

    }
}
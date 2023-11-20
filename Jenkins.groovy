pipeline {
    agent any
    stages {
        stage('Download Repository Files') {
            steps {
                // clone the repository to a local folder
                dir('git_repo') {
                    git(url: 'git@github.com:denisprohodski/development.git', branch: 'main')
                }
            }
        }
 
        stage('Checkout') {
            steps {
                // Check out source code
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                // Install required dependencies
                sh '''
                    python3 -m venv env
                    . env/bin/activate
                    python3 -m pip install -r requirements.txt
                '''
            }
        }
        stage('Run Tests') {
            steps {
                // Run your pytest tests
                sh '''	
                    . env/bin/activate
                    pytest --junitxml=results.xml test_cases.py
                '''
            }
        }
        stage('Push to Release Branch') {
            steps {
                dir('git_repo') {
                    sh '''
                        git push origin main:release
                    '''
                }
            }
        }
    }
}
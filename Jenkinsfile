pipeline {
    agent any
    environment {
        HOST = ${HOST}
        USER = ${USERNAME}
        PASS = ${PASSWORD}
        BUCKET_NAME = ${BUCKET_NAME}
    }
    // triggers {
    //     cron('H */4 * * 1-5')
    // }
    stages {
        stage('Python Lint') {
            steps {
                sh 'pylint shipup-s3-transfer.py'
            }
        }
        stage('Install pip requirements') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Transfer csv files to S3') {
            steps {
                sh '''
                python3 shipup-s3-transfer.py
                echo 'Transfer successful'
                '''
                
            }
        }
    }
}

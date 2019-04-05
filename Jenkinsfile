pipeline {
    agent any
    environment {
        HOST = $HOST
        USER = $USERNAME
        PASS = $PASSWORD
    }
    // triggers {
    //     cron('H */4 * * 1-5')
    // }
    stages {
        stage('Transfer csv files to S3') {
            steps {
                python3 shipup-s3-transfer.py
            }
        }
    }
}

pipeline {
    agent any

    stages {
        
        stage('BuildInDev') {
            steps {
                build job: 'build-mat-dev', parameters: [string(name: 'BUILD_ID', value: env.BUILD_ID)]
            }
        }
        stage('DeployInDev') {
            steps {
                build job: 'deploy-mat-dev', parameters: [string(name: 'BUILD_ID', value: env.BUILD_ID)]
            }
        }
    }
}
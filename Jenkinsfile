pipeline {
    agent any
    environment {
        PYTHON_EXECUTABLE = '/usr/bin/python3.4'
        VIRTUAL_ENVIRONMENT_DIRECTORY = 'env'
        ENVIRONMENT_STAGING = 'staging'
        EXTRA_INDEX_URL = 'https://pypi.cherubits.hu'
        SUDO_PASSWORD = 'Armageddon0'
        SLACK_BASE_URL = 'https://cherubits.slack.com/services/hooks/jenkins-ci/'
    }
    stages {
        stage('Initialize') {
            steps {
                slackSend color: 'good', message: "$JOB_NAME started new build $env.BUILD_NUMBER (<$BUILD_URL|Open>)", baseUrl: "$SLACK_BASE_URL", botUser: true, channel: 'jenkins', teamDomain: 'cherubits', tokenCredentialId: 'cherubits-slack-integration-token'
                git([url: '${GIT_URL}', branch: '$GIT_BRANCH', changelog: true, credentialsId: 'jenkins-private-key', poll: true])
            }
        }

        stage('Setup') {
              steps {
                echo 'Setup virtual environment'
                sh '''if [ ! -d "$VIRTUAL_ENVIRONMENT_DIRECTORY" ]; then
                        virtualenv --no-site-packages -p $PYTHON_EXECUTABLE $VIRTUAL_ENVIRONMENT_DIRECTORY
                    fi
                '''
              }
        }

        stage('Build') {
            steps {
                echo 'Install requirements'
                sh '''. ./env/bin/activate
                    pip install -r ./requirements-full.txt --extra-index-url=$EXTRA_INDEX_URL
                    deactivate
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            when {
              expression {
                currentBuild.result == null || currentBuild.result == 'SUCCESS'
              }
            }
            steps {
                echo 'Install locally'
                sh '''. ./env/bin/activate
                    python setup.py sdist install
                    deactivate
                '''
                echo 'Update version'
                sh '''. ./env/bin/activate
                    RC_VERSION=$(cat $DJANGO_PROJECT/version.py | grep "__version__ = " | sed 's/__version__ =//' | tr -d "'")
                    bumpversion --allow-dirty --message 'Jenkins Build {$BUILD_NUMBER} bump version: {current_version} -> {new_version}' --commit --current-version $RC_VERSION patch $DJANGO_PROJECT/version.py
                    deactivate
                '''
                sh '''git push origin ${GIT_BRANCH}
                '''
                slackSend color: 'good', message: "$JOB_NAME $env.BUILD_NUMBER published a new version (<$BUILD_URL|Open>)", baseUrl: "$SLACK_BASE_URL", botUser: true, channel: 'jenkins', teamDomain: 'cherubits', tokenCredentialId: 'cherubits-slack-integration-token'
            }
        }
        stage('Distribute') {
            when {
              expression {
                currentBuild.result == null || currentBuild.result == 'SUCCESS'
              }
            }
            steps {
                echo 'Publish distribution'
                sh '''. ./env/bin/activate
                    python setup.py sdist upload -r local
                    deactivate
                '''
                slackSend color: 'good', message: "$JOB_NAME $env.BUILD_NUMBER deployed (<$BUILD_URL|Open>)", baseUrl: "$SLACK_BASE_URL", botUser: true, channel: 'jenkins', teamDomain: 'cherubits', tokenCredentialId: 'cherubits-slack-integration-token'
            }
        }
    }
    post {
        failure {
            slackSend color: 'danger', message: "$JOB_NAME $env.BUILD_NUMBER failed. (<$BUILD_URL|Open>)", baseUrl: "$SLACK_BASE_URL", botUser: true, channel: 'jenkins', teamDomain: 'cherubits', tokenCredentialId: 'cherubits-slack-integration-token'
        }
    }
}
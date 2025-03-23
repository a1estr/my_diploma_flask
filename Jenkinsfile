pipeline {
    agent any

    environment {
        ALLURE_RESULTS_DIR = 'allure-results'
        TELEGRAM_API_TOKEN = '7444074270:AAHIu2OqOaIUTr7X2VOoiI-kmtT21V8k7HM'
        TELEGRAM_CHAT_ID = '205318699'
        COVERAGE_REPORT_DIR = 'coverage-report'
    }

    stages {

        stage('Build and Start Services') {
            steps {
                script {
                    // Задаем переменную MY_APP_DIR
                    env.MY_APP_DIR = "/var/lib/docker/volumes/jenkins-data-flask/_data/workspace/${env.JOB_NAME}"
                    echo "MY_APP_DIR is ${env.MY_APP_DIR}"
                    // Выполняем команду в оболочке; переменная MY_APP_DIR будет доступна благодаря env.
                    sh """
                        echo "Using MY_APP_DIR: \$MY_APP_DIR"
                        docker compose up --build web db -d
                    """
                }
            }
        }


        stage('Prepare Allure Results Directory') {
            steps {
                script {
                    // Cоздаем директорию для результатов Allure
                    sh "mkdir -p ${env.ALLURE_RESULTS_DIR}"
                }
            }
        }

        stage('Run Database Connection Test') {
            steps {
                script {
                    // Запускаем тестовый сервис для проверки подлючения к БД
                    sh "docker compose run --rm -e TEST_PATH=tests/test_db_connection.py -e TEST_ARGS='--alluredir=${env.ALLURE_RESULTS_DIR}' test"
                }
            }
        }

        stage('Run API Tests') {
            steps {
                script {
                    // Запускаем тестовый сервис для тестирования API
                    sh "docker compose run --rm -e TEST_PATH=tests/api -e TEST_ARGS='--alluredir=${env.ALLURE_RESULTS_DIR}' test"
                }
            }
        }

        stage('Run UI Tests') {
            steps {
                script {
                    // Запускаем тестовый сервис для тестирования UI
                    sh "docker compose run --rm -e TEST_PATH=tests/ui -e TEST_ARGS='--alluredir=${env.ALLURE_RESULTS_DIR}' test"
                }
            }
        }

        stage('Generate Test Coverage Report') {
            steps {
                script {
                    // Генерация отчета о покрытии тестов
                    sh "docker compose run --rm -e TEST_PATH=src -e TEST_ARGS='--cov=src --cov-report=xml --cov-report=html:${env.COVERAGE_REPORT_DIR}' test"
                }
            }
        }
    }

    post {
        always {
            script {
                def resultsExist = sh(returnStatus: true, script: """
                    [ -d ${env.ALLURE_RESULTS_DIR} ] && [ \"\$(ls -A ${env.ALLURE_RESULTS_DIR})\" ]
                """) == 0

                def statusMessage = "Build finished with status: ${currentBuild.result}"
                if (currentBuild.result == 'SUCCESS') {
                    statusMessage = "Tests passed successfully in ${env.JOB_NAME}."
                } else {
                    statusMessage = "Tests failed in ${env.JOB_NAME}. Please check the logs."
                }

                // Отправка уведомления в Telegram
                sh """
                    curl -s -X POST https://api.telegram.org/bot${env.TELEGRAM_API_TOKEN}/sendMessage \
                    -d chat_id=${env.TELEGRAM_CHAT_ID} \
                    -d text="${statusMessage}"
                """

                if (resultsExist) {
                    echo 'Allure results found. Generating report...'
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: "${env.ALLURE_RESULTS_DIR}"]]
                    ])
                } else {
                    echo 'No Allure results found. Tests might not have run.'
                }
            }
        }

        cleanup {
            echo 'Cleaning up...'
            sh """
            docker compose down
            rm -rf allure.zip ${env.ALLURE_RESULTS_DIR}
            """
            deleteDir()
        }
    }
}

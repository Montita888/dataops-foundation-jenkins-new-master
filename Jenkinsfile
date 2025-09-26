pipeline {
    agent any
    
    environment {
        DB_SERVER = '34.30.35.116'
        DB_NAME = 'TestDB'
        DB_USERNAME = 'SA'
        DB_PASSWORD = credentials('mssql-password')
        PYTHON_VERSION = '3.9'
        VIRTUAL_ENV = 'venv'
        DATA_FILE = 'data/LoanStats_web_small.csv'
        MAX_NULL_PERCENTAGE = '30'
        MIN_YEAR = '2016'
        MAX_YEAR = '2019'
    }
    
    options {
        buildDiscarder(logRotator(daysToKeepStr: '30', numToKeepStr: '20'))
        timeout(time: 20, unit: 'MINUTES')
        timestamps()
    }
    
    stages {
        stage('🔄 Checkout & Setup') {
            steps {
                script {
                    echo "=== Simple ETL CI/CD Pipeline Started ==="
                    echo "Build: ${BUILD_NUMBER}"
                    echo "Branch: ${env.GIT_BRANCH ?: 'main'}"
                    echo "Workspace: ${WORKSPACE}"
                }
                script {
                    if (!fileExists('functions/__init__.py')) { error "❌ Functions package not found!" }
                    if (!fileExists('etl_pipeline.py')) { error "❌ ETL pipeline script not found!" }
                    echo "✅ Project structure verified"
                }
            }
        }
        
        stage('🐍 Python Environment') {
            steps {
                script { echo "Setting up Python environment..." }
                sh '''
                    rm -rf ${VIRTUAL_ENV}
                    python3 -m venv ${VIRTUAL_ENV}
                    . ${VIRTUAL_ENV}/bin/activate
                    python -m pip install --upgrade pip
                    pip install pandas numpy sqlalchemy pymssql
                    pip install pytest pytest-cov
                    python -c "import pandas, numpy, sqlalchemy; print('✅ Core packages installed')"
                    python --version
                '''
            }
        }
        
        stage('🧪 Unit Tests') {
            parallel {
                stage('Test: guess_column_types') {
                    steps {
                        script { echo "Testing guess_column_types function..." }
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            cd tests
                            python guess_column_types_test.py
                        '''
                    }
                }
                stage('Test: filter_issue_date_range') {
                    steps {
                        script { echo "Testing filter_issue_date_range function..." }
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            cd tests
                            python filter_issue_date_range_test.py
                        '''
                    }
                }
                stage('Test: clean_missing_values') {
                    steps {
                        script { echo "Testing clean_missing_values function..." }
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            cd tests
                            python clean_missing_values_test.py
                        '''
                    }
                }
            }
        }
        
        stage('🔍 ETL Validation') {
            when { expression { currentBuild.result != 'FAILURE' } }
            steps {
                script { echo "Validating ETL pipeline components..." }
                sh '''
                    . ${VIRTUAL_ENV}/bin/activate
                    python -c "
from functions import guess_column_types, filter_issue_date_range, clean_missing_values
print('✅ All functions imported successfully')
"
                    if [ -f "${DATA_FILE}" ]; then
                        echo "✅ Data file found: ${DATA_FILE}"
                        python -c "
import pandas as pd
df = pd.read_csv('${DATA_FILE}', low_memory=False, nrows=10)
print(f'✅ Data file readable: {len(df.columns)} columns')
"
                    else
                        echo "⚠️  Data file not found: ${DATA_FILE}"
                    fi
                '''
            }
        }
        
        stage('🔄 ETL Processing') {
            when { expression { currentBuild.result != 'FAILURE' } }
            steps {
                script { echo "Running ETL pipeline with sample data..." }
                sh '''
                    . ${VIRTUAL_ENV}/bin/activate
                    python etl_pipeline.py
                '''
            }
        }
        
        stage('📤 Deploy to Database') {
            when { expression { currentBuild.result != 'FAILURE' } }
            steps {
                script { echo "Deploying to database..." }
                sh '''
                    . ${VIRTUAL_ENV}/bin/activate
                    python etl_pipeline.py --deploy
                '''
            }
        }

        // ✅ ทำความสะอาดที่นี่ แทนที่จะไปทำใน post (จะได้ไม่ไปติดรอคิว)
        stage('🧹 Cleanup') {
            steps {
                script { echo "Cleaning up workspace and venv..." }
                sh '''
                    rm -rf ${VIRTUAL_ENV} || echo "Virtual environment cleanup completed"
                    find . -name "*.pyc" -delete 2>/dev/null || echo "Python cache cleaned"
                    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || echo "Pycache cleaned"
                '''
                // หรือถ้าใช้ปลั๊กอิน Workspace Cleanup:
                // cleanWs()
            }
        }
    }
    
    post {
        always {
            echo "=== Pipeline Completed ==="
            echo "Build Number: ${BUILD_NUMBER}"
            echo "Duration: ${currentBuild.durationString}"
            echo "Result: ${currentBuild.result ?: 'SUCCESS'}"
        }
        success {
            echo """
🎉 ETL Pipeline succeeded!
✅ All tests passed
✅ ETL processing completed
✅ Deployed to MSSQL database

Build: ${BUILD_NUMBER}
Duration: ${currentBuild.durationString}
"""
        }
        failure {
            echo """
❌ ETL Pipeline failed!

Build: ${BUILD_NUMBER}
Duration: ${currentBuild.durationString}

Please check the console output for details.
"""
        }
        unstable {
            echo "⚠️  ETL Pipeline unstable - some tests may have failed"
        }
    }
}

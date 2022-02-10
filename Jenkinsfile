def usernames = "return['marvin-trezlabs','luis-trezlabs','nirgeier']";

//Script for the branch, you can reference the previous script value witn the "REPO" variable
def credsId = """def credsNames = []

def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
    com.cloudbees.plugins.credentials.Credentials.class
)

def credsIds = [];
credsIds.push('None');
for (cred in creds) {
    credsIds.push(cred.id)
}

return credsIds;""";

def dates = """return[
'1 week',
'2 weeks',
'1 month',
'3 months',
'1 year',
'2 years',
'All dates'
]""";


pipeline {
    agent any
    stages {
        stage('Parameters'){
            steps {
                script {
                properties([
                        //Creating the parameters, make sure you have Active Choice plugin installed
                        parameters([  
                            [$class: 'ChoiceParameter', 
                                //Single combo-box item select type of choice
                                choiceType: 'PT_SINGLE_SELECT', 
                                description: 'Select the github account', 
                                filterLength: 1, 
                                filterable: false, 
                                //Important for identify it in the cascade choice parameter and the params. values
                                name: 'USERNAME', 
                                script: [
                                    $class: 'GroovyScript', 
                                    //Error script
                                    fallbackScript: [
                                        classpath: [], 
                                        sandbox: false, 
                                        script: 
                                            "return['No accounts registered on pipeline']"
                                    ], 
                                    script: [
                                        classpath: [], 
                                        sandbox: false, 
                                        //Calling local variable with the script as a string
                                        script: "${usernames}"
                                        
                                    ]
                                ]
                            ],
                            [$class: 'ChoiceParameter', 
                                //Single combo-box item select type of choice
                                choiceType: 'PT_SINGLE_SELECT', 
                                description: 'Select the credentialID for the Personal Access Token (optional) - Secret Text Type expeceted', 
                                filterLength: 1, 
                                filterable: true, 
                                //Important for identify it in the cascade choice parameter and the params. values
                                name: 'CREDENTIAL', 
                                script: [
                                    $class: 'GroovyScript', 
                                    //Error script
                                    fallbackScript: [
                                        classpath: [], 
                                        sandbox: false, 
                                        script: 
                                            "return['Could not get the credentials IDs']"
                                    ], 
                                    script: [
                                        classpath: [], 
                                        sandbox: false, 
                                        //Calling local variable with the script as a string
                                        script: "${credsId}"
                                        
                                    ]
                                ]
                            ],
                            [$class: 'ChoiceParameter', 
                                //Single combo-box item select type of choice
                                choiceType: 'PT_SINGLE_SELECT', 
                                description: 'Select the github account', 
                                filterLength: 1, 
                                filterable: false, 
                                //Important for identify it in the cascade choice parameter and the params. values
                                name: 'DATE', 
                                script: [
                                    $class: 'GroovyScript', 
                                    //Error script
                                    fallbackScript: [
                                        classpath: [], 
                                        sandbox: false, 
                                        script: 
                                            "return['No dates registered on pipeline']"
                                    ], 
                                    script: [
                                        classpath: [], 
                                        sandbox: false, 
                                        //Calling local variable with the script as a string
                                        script: "${dates}"
                                        
                                    ]
                                ]
                            ]
                        ])
                    ])
                }
            }
        }
        stage('checkout scm') {
            steps {
                //Changing workdir to the previous dir created
                git branch: "testing", 
                    poll: false, 
                    url: "https://github.com/marvin-trezlabs/branches-automation.git"
            }
        }
        stage('Test') {
            steps {
                sh 'mkdir -p json-reports'
                sh 'mkdir -p mails'
                withCredentials([string(credentialsId: "${params.CREDENTIAL}", variable: 'GITHUB_TOKEN')]) {
                    sh "python3 script.py --date='${params.DATE}' --base-branch=main --report-id=${BUILD_NUMBER} --username=${params.USERNAME}"
                    // env.REPORT=sh([script: "python3 script.py --date=2022-02-10 --base-branch=main", returnStdout: true ]).trim()
                }
                script {  
                    fileContents = readFile "./mails/mail-${BUILD_NUMBER}.txt"
                    print("Sending report JSON ID:${BUILD_NUMBER}")
                }
            }
        }

        stage('Sending mail') {
            steps {
                mail to: 'user@mydomain.com',               
                    subject: "Sending report of old merged branches" ,
                    body: """${fileContents}"""
            }
        }
    }   
}
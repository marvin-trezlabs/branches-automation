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

def repoScript = """import groovy.json.JsonSlurper

def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
      com.cloudbees.plugins.credentials.Credentials.class
)

token = 'none'

for (cred in creds) {
    if(cred.id == CREDENTIAL && cred.hasProperty('secret')){
        token = cred.secret
    }
}

def get;
if(token != 'none'){
    get = new URL("https://api.github.com/user/repos").openConnection();
    get.setRequestProperty("Authorization", 'token ' + token);
}else {
    get = new URL("https://api.github.com/users/" + USERNAME +"/repos").openConnection();
}

def getRC = get.getResponseCode();

if (getRC.equals(200)) {
    def json = get.inputStream.withCloseable { inStream ->
        new JsonSlurper().parse( inStream as InputStream )
    }

    def item = json;
    def names = [];

    item.each { repo ->
        names.push(repo.name);
    }   
    return names;
}""";

def dates = """return[
'1 week',
'2 weeks',
'1 month',
'3 months',
'1 year',
'2 years',
'All dates'
]""";

def getReport = """import groovy.json.JsonSlurper

if (JSON_REPORT_ID){

def filepath = "/var/jenkins_home/workspace/test/json-reports/" + JSON_REPORT_ID + ".json"

return "cat ${filepath}".execute().text

} else {
return ""
}""";


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
                               [$class: 'CascadeChoiceParameter', 
                                //Single combo-box item select type of choice
                                choiceType: 'PT_SINGLE_SELECT', 
                                description: 'Select the Repository from the Dropdown List', 
                                filterLength: 1, 
                                filterable: true, 
                                referencedParameters: 'CREDENTIAL, USERNAME', 
                                //Important for identify it in the cascade choice parameter and the params. values
                                name: 'REPO', 
                                script: [
                                    $class: 'GroovyScript', 
                                    //Error script
                                    fallbackScript: [
                                        classpath: [], 
                                        sandbox: false, 
                                        script: 
                                            "return['Could not get The Repos']"
                                    ], 
                                    script: [
                                        classpath: [], 
                                        sandbox: false, 
                                        //Calling local variable with the script as a string
                                        script: "${repoScript}"
                                        
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
                            ],
                            string(name: 'MAIL', defaultValue: '', description: 'Optional: Mail direction to send the report. Leave blank for not sending\n\n\n\n TO DELETE: \n IF U ALREADY GENERATED A JSON PLAN '),
                            string(name: 'JSON_REPORT_ID', defaultValue: '', description: 'DANGEROUS: Provide the ID of a previous report to for DELETING the branches'),
                            booleanParam(name: 'CONFIRM_DELETE', defaultValue: false, description: 'DANGEROUS: Confirm delete of the previous REPORT ID'),
                            [$class: 'DynamicReferenceParameter',
                                choiceType: 'ET_FORMATTED_HTML',
                                // omitValueField: true,
                                name: '',
                                referencedParameters: 'JSON_REPORT_ID',
                                script: [
                                    $class: 'GroovyScript',
                                    fallbackScript: [
                                            classpath: [],
                                            sandbox: true,
                                            script:
                                            'return[\'ERROR or Report doesnt exist on filesystem...\']'
                                    ],
                                    script: [
                                        classpath: [],
                                        sandbox: false,
                                        script:"${getReport}"
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
                // Needed directories for the python script to store the mail and json
                sh 'mkdir -p json-reports'
                sh 'mkdir -p mails'
                withCredentials([string(credentialsId: "${params.CREDENTIAL}", variable: 'GITHUB_TOKEN')]) {
                    sh "python3 script.py --date='${params.DATE}' --base-branch=main --report-id=${params.REPO}-${BUILD_NUMBER} --username=${params.USERNAME} --repo=${params.REPO}"
                    // env.REPORT=sh([script: "python3 script.py --date=2022-02-10 --base-branch=main", returnStdout: true ]).trim()
                }
                script {  
                    mailContent = readFile "mails/mail-${params.REPO}-${BUILD_NUMBER}.txt"
                    print("Report JSON ID:${params.REPO}-${BUILD_NUMBER}")
                }
            }
        }

        stage('Sending mail') {
            steps {
                script {
                    if(params.MAIL){
                        mail to: params.MAIL,               
                            subject: "Sending report of old merged branches" ,
                            body: """${mailContent}"""
                    }
                }

            }
        }
    }   
}
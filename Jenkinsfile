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

def filepath = "/var/jenkins_home/workspace/branch-cleaner/json-reports/" + JSON_REPORT_ID + ".json"
def command = "cat " + filepath
def branches = command.execute().text 
if (branches) {
def html = "<p style='color:red;'>This action will delete the folowing branches: </p><p style='color:gray;'>" + branches + "</p>"
return html
}else{
return "<p style='color:gray;'> Report not found </p>"
}

} else {
return ""
}""";

def branchScript = """import groovy.json.JsonSlurper

def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
      com.cloudbees.plugins.credentials.Credentials.class
)

def token = 'none'

for (cred in creds) {
    if(cred.id == CREDENTIAL && cred.hasProperty('secret')){
        token = cred.secret
    }
}

def getBranches;
getBranches = new URL("https://api.github.com/repos/" + USERNAME +"/" + REPO + "/branches").openConnection();

if(token != 'none'){
    getBranches.setRequestProperty("Authorization", 'token ' + token);
}

def getRCBranches = getBranches.getResponseCode();

if (getRCBranches.equals(200)) {
   def jsonBr = getBranches.inputStream.withCloseable { inStream ->
           new JsonSlurper().parse( inStream as InputStream )
   }

    def itemBr = jsonBr;
    def namesBr = [];

    itemBr.each { branch ->
        namesBr.push(branch.name);
    } 
    return namesBr;
}""";


pipeline {
    agent {
        node {
            label 'linux-node'
            customWorkspace 'workspace/branch-cleaner'
        }
    }
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
                            [$class: 'CascadeChoiceParameter', 
                                choiceType: 'PT_SINGLE_SELECT', 
                                description: 'Select the Branch from the Dropdown List',
                                name: 'BASE_BRANCH',                                
                                filterable: true, 
                                //Referencing the repo
                                referencedParameters: 'REPO, CREDENTIAL, USERNAME', 
                                script: 
                                    [$class: 'GroovyScript', 
                                    fallbackScript: [
                                            classpath: [], 
                                            sandbox: false, 
                                            script: "return['Could not get Branch from the Repo']"
                                            ], 
                                    script: [
                                            classpath: [], 
                                            sandbox: false, 
                                            //branchScript variable
                                            script: "${branchScript}"
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
                            ],
                            booleanParam(name: 'CONFIRM_DELETE', defaultValue: false, description: 'DANGEROUS: Confirm delete of the previous REPORT ID')
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
        stage('Python search') {
            when { expression { params.JSON_REPORT_ID == '' } }
            steps {
                // Needed directories for the python script to store the mail and json
                sh 'mkdir -p json-reports'
                sh 'mkdir -p mails'
                withCredentials([string(credentialsId: "${params.CREDENTIAL}", variable: 'GITHUB_TOKEN')]) {
                    sh "python3 script.py --date='${params.DATE}' --base-branch=${params.BASE_BRANCH} --report-id=${params.REPO}-${BUILD_NUMBER} --username=${params.USERNAME} --repo=${params.REPO}"
                    // env.REPORT=sh([script: "python3 script.py --date=2022-02-10 --base-branch=main", returnStdout: true ]).trim()
                }
                script {  
                    mailContent = readFile "mails/mail-${params.REPO}-${BUILD_NUMBER}.txt"
                }
            }
        }

        stage('Sending mail') {
            when { expression { params.JSON_REPORT_ID == '' } }
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

        stage('Deleting branches if ID was provided') {
            when { expression { params.JSON_REPORT_ID != '' } }
            steps {
                script {
                    if(params.JSON_REPORT_ID && params.CONFIRM_DELETE){
                        withCredentials([string(credentialsId: "${params.CREDENTIAL}", variable: 'GITHUB_TOKEN')]) {
                            sh "python3 delete.py --report-id=${params.JSON_REPORT_ID} --username=${params.USERNAME}"
                            // env.REPORT=sh([script: "python3 script.py --date=2022-02-10 --base-branch=main", returnStdout: true ]).trim()
                        }
                    }
                }

            }
        }
    }   
}
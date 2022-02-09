pipeline {
    agent any
    stages {
        // stage('Parameters'){
        //     steps {
        //         script {
        //         properties([
        //                 //Creating the parameters, make sure you have Active Choice plugin installed
        //                 parameters([  [$class: 'ChoiceParameter', 
        //                         //Single combo-box item select type of choice
        //                         choiceType: 'PT_SINGLE_SELECT', 
        //                         description: 'Select the github account', 
        //                         filterLength: 1, 
        //                         filterable: false, 
        //                         //Important for identify it in the cascade choice parameter and the params. values
        //                         name: 'USERNAME', 
        //                         script: [
        //                             $class: 'GroovyScript', 
        //                             //Error script
        //                             fallbackScript: [
        //                                 classpath: [], 
        //                                 sandbox: false, 
        //                                 script: 
        //                                     "return['No accounts registered on pipeline']"
        //                             ], 
        //                             script: [
        //                                 classpath: [], 
        //                                 sandbox: false, 
        //                                 //Calling local variable with the script as a string
        //                                 script: "${usernames}"
                                        
        //                             ]
        //                         ]
        //                     ],
        //                     [$class: 'ChoiceParameter', 
        //                         //Single combo-box item select type of choice
        //                         choiceType: 'PT_SINGLE_SELECT', 
        //                         description: 'Select the credentialID for the Personal Access Token (optional) - Secret Text Type expeceted', 
        //                         filterLength: 1, 
        //                         filterable: true, 
        //                         //Important for identify it in the cascade choice parameter and the params. values
        //                         name: 'CREDENTIAL', 
        //                         script: [
        //                             $class: 'GroovyScript', 
        //                             //Error script
        //                             fallbackScript: [
        //                                 classpath: [], 
        //                                 sandbox: false, 
        //                                 script: 
        //                                     "return['Could not get the credentials IDs']"
        //                             ], 
        //                             script: [
        //                                 classpath: [], 
        //                                 sandbox: false, 
        //                                 //Calling local variable with the script as a string
        //                                 script: "${credsId}"
                                        
        //                             ]
        //                         ]
        //                     ],
        //                     [$class: 'CascadeChoiceParameter', 
        //                         //Single combo-box item select type of choice
        //                         choiceType: 'PT_SINGLE_SELECT', 
        //                         description: 'Select the Repository from the Dropdown List', 
        //                         filterLength: 1, 
        //                         filterable: true, 
        //                         referencedParameters: 'CREDENTIAL, USERNAME', 
        //                         //Important for identify it in the cascade choice parameter and the params. values
        //                         name: 'REPO', 
        //                         script: [
        //                             $class: 'GroovyScript', 
        //                             //Error script
        //                             fallbackScript: [
        //                                 classpath: [], 
        //                                 sandbox: false, 
        //                                 script: 
        //                                     "return['Could not get The Repos']"
        //                             ], 
        //                             script: [
        //                                 classpath: [], 
        //                                 sandbox: false, 
        //                                 //Calling local variable with the script as a string
        //                                 script: "${repoScript}"
                                        
        //                             ]
        //                         ]
        //                     ],
        //                     //Cascade choice, means you can reference other choice values, like in this case, the REPO
        //                     //Also, re-runs this scripts every time the referenced choice value changes.
        //                     [$class: 'CascadeChoiceParameter', 
        //                         choiceType: 'PT_SINGLE_SELECT', 
        //                         description: 'Select the Branch from the Dropdown List',
        //                         name: 'BRANCH',                                
        //                         filterable: true, 
        //                         //Referencing the repo
        //                         referencedParameters: 'REPO, CREDENTIAL, USERNAME', 
        //                         script: 
        //                             [$class: 'GroovyScript', 
        //                             fallbackScript: [
        //                                     classpath: [], 
        //                                     sandbox: false, 
        //                                     script: "return['Could not get Branch from the Repo']"
        //                                     ], 
        //                             script: [
        //                                     classpath: [], 
        //                                     sandbox: false, 
        //                                     //branchScript variable
        //                                     script: "${branchScript}"
        //                             ] 
        //                         ]
        //                     ]
        //                 ])
        //             ])
        //         }
        //     }
        // }
        stage('checkout scm') {
            steps {
                //Changing workdir to the previous dir created
                git branch: "main", 
                    poll: false, 
                    url: "https://github.com/marvin-trezlabs/branches-automation.git"
            }
        }
        
        stage('Test') {
            steps {
                //BUilding the image
                // sh "docker build -t ${params.REPO}:latest ."
                // TAggin the image to the latest and the current build tag
                // sh "docker tag ${params.REPO} ${dockerHubUser}/${params.REPO}:latest"
                // sh "docker tag ${params.REPO} ${dockerHubUser}/${params.REPO}:$BUILD_NUMBER"

                withCredentials([string(credentialsId: 'github-token', variable: 'TOKEN')]) {
                    sh '''
                        export GITHUB_TOKEN=$TOKEN
                        python3 script.py --date=2022-02-10 --base-branch=main
                    '''
                }

            }
        }
        // stage('Publish image to Docker Hub') {
        //     steps {
        //         dir(path: "${params.REPO}"){
        //             //Using docker push plugin and dockerhub credentials, blank url for docker hub registry
        //             //Uses docker-pipeline plugin
        //             withDockerRegistry([credentialsId: "dockerHub", url: ""]) {
        //                 //Pushing both (latest and build number image)
        //                 sh "docker push ${dockerHubUser}/${params.REPO}:latest"
        //                 sh "docker push ${dockerHubUser}/${params.REPO}:$BUILD_NUMBER"
        //             }
        //         }
        //     }
        // }
    }   
}
#!/usr/bin/env python3
import os
import requests
import argparse
from datetime import datetime, timedelta

parser = argparse.ArgumentParser()

# Defining arguments
# parser.add_argument("--dryrun", help="Set this flag to True to run in safe/report mode", dest='dryrun', action='store_true')
parser.add_argument("--date", help="<Required> Date umbral", type=str)
parser.add_argument("--base-branch", help="<Optional>  Define the base branch of the search criteria. Default: main", dest='baseBranch', type=str)
parser.add_argument("--delete-all", help="<Optional> Set this flag to delete all the matched branches", dest='deleteall', action='store_true')
parser.add_argument('-p','--protect', default=["master"], nargs='+', dest='protected', help='<Optional> Flag to protect specific branches of being delete by flag --delete-all')
parser.set_defaults(deleteall=False, baseBranch="main")

args = parser.parse_args()

# Getting Token from ENV
token = os.getenv('GITHUB_TOKEN', '...')
# Variables (Maybe convert to ENV)
owner = "marvin-trezlabs"
repo = "GitPracticeRepo"

# Formating date
date = args.date + 'T0:0:0Z'
umbralDate = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")

# Getting criteria from params
userWantsToDelete = True if args.deleteall == True else False
baseBranch = args.baseBranch
protectedBranches = args.protected
# isDryRun = True if args.dryrun == True else False

# Setting authorization headers
headers = {'Authorization': f'token {token}'}

# Fetching branches
url = "https://api.github.com/repos/" + owner +"/"+ repo + "/branches"
response = requests.get(url, headers=headers)
branches = response.json()

if(response.status_code != 200 ) :
    print('Credentials or connection error')
    exit()

# Printing info
print('Criteria:')
print( '  Delete: True' if userWantsToDelete == True else '  Dry-Run / Report mode (Pass the --delete-all flag to delete merged branches)')
# print('  Is dry run: ' + str(isDryRun))
print('  Date: Older than: ' + str(umbralDate))
print("  Protected branches: ", *protectedBranches, sep = " | ") 
print('\n🔍 Searching.........\n')


# empty results variable
branchesFound = []

# Looping branches 
for br in branches:
    branchName = br['name']
    # Fetching the head commit in order to get the latest commit date
    response2 = requests.get(br['commit']['url'], headers=headers)
    jsondata = response2.json()

    # Extracting the date 
    branchDate = jsondata['commit']['author']['date']
    branchDate = datetime.strptime(branchDate, "%Y-%m-%dT%H:%M:%S%z")
    
    #  Checking if the date is in the interval
    if(branchDate <= umbralDate) :    

        # Fetching the pull requests of that branches to determine if was merged or not
        url = "https://api.github.com/repos/" + owner + "/" + repo + "/pulls?state=all&base=" + baseBranch + "&head="+ owner + ":" + branchName
        response3 = requests.get(url, headers=headers)
        pullRequests = response3.json()
        
        # Looping PR 
        for pullRequest in pullRequests:
            # Extracting if was merged bool 
            wasMerged = bool(pullRequest['merged_at']) if pullRequest['merged_at'] else False
            if(wasMerged):
                # pprint.pprint(pullRequest)
                # Not show empty search message
                branchesFound.append(br['name'])
                # Printing info 
                if br['name'] in protectedBranches:
                    print('\033[94m<Protected>\033[0m')
                print('Found BRANCH: ' + br['name'])
                print(' -- Pull Request title: ' + pullRequest['title'] )
                print(" -- Merged at date: " + pullRequest['merged_at'] + ', to base branch: ' + pullRequest['base']['ref'] +'\n')

            if br['name'] not in protectedBranches:
                # Checking flags to determine if proceed to delete
                if(wasMerged == True and userWantsToDelete == True) :
                    # Deleting the branch
                    urlDelete = "https://api.github.com/repos/"+ owner + "/" + repo + "/git/refs/heads/" + branchName
                    responseDelete = requests.delete(urlDelete, headers=headers)
                    print('deleting merged branch...')
                    if(responseDelete.status_code) :
                        print('✔ Deleted successfully')
                    else :
                        print('✖ Failed to delete')
                    break

# Empty results
if(len(branchesFound) <=0 ):
    print('NOT found branches that match the Criteria')



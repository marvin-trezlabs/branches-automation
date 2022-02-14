#!/usr/bin/env python3
import json
import os
import requests
import argparse
from datetime import datetime, timedelta

parser = argparse.ArgumentParser()

# Defining arguments
# parser.add_argument("--dryrun", help="Set this flag to True to run in safe/report mode", dest='dryrun', action='store_true')
parser.add_argument("--date", help="<Required> Date umbral", type=str)
parser.add_argument("--base-branch", help="<Optional>  Define the base branch of the search criteria. Default: main", dest='baseBranch', type=str)
parser.add_argument('-p','--protect', default=["main"], nargs='+', dest='protected', help='<Optional> Flag to protect specific branches of being delete by flag --delete-all')
parser.add_argument("--report-id", help="<Optional>  Define the report ID", dest='reportId', type=str)
parser.add_argument("--username", help="Define the Username", dest='username', type=str)
parser.add_argument("--repo", help="Define the Repo", dest='repo', type=str)

parser.set_defaults(baseBranch="main")

args = parser.parse_args()

# Getting Token from ENV
token = os.getenv('GITHUB_TOKEN', '...')
# Variables (Maybe convert to ENV)
owner = args.username
repo = args.repo

# Formating date
umbralDate = ''

# Reading the paramenters and converting to specific iso time
def convertDate(days):
    global umbralDate
    d = datetime.today() - timedelta(days=days)
    umbralDate = d.strftime("%Y-%m-%dT%H:%M:%S%z")
    # Just to match the format from github
    umbralDate = umbralDate + 'Z'
    umbralDate = datetime.strptime(umbralDate, "%Y-%m-%dT%H:%M:%S%z")

if(args.date == '1 week'):
    convertDate(7)
elif(args.date == '2 weeks'):
    convertDate(14)
elif(args.date == '1 month'):
    convertDate(30)
elif(args.date == '3 months'):
    convertDate(60)
elif(args.date == '1 year'):
    convertDate(365)
elif(args.date == '2 years'):
    convertDate(730)
elif(args.date == 'All dates'):
    convertDate(0)
else:
    print('ERROR: No matches with that date on local array')
    exit()

# Getting criteria from params
baseBranch = args.baseBranch
protectedBranches = args.protected

# Setting authorization headers
headers = {'Authorization': f'token {token}'}
# empty results variable
branchesFound = []
page = 1;
fetchAgain = True;
branches = {}

# Printing info
print('Criteria:')
# print('  Is dry run: ' + str(isDryRun))
print('  Date: Older than: ' + str(umbralDate))
print("  Protected branches: ", *protectedBranches, sep = " | ") 
print('\n🔍 Searching.........\n')

# BUILDING THE EMAIL STRUCTURE: 
# a if for append mode
with open('mails/mail-' + args.reportId + '.txt', 'a') as f:
    f.write('\nOLD BRANCHES REPORT\n')
    f.write('Json ID:' + args.reportId +'\n')
    f.write('Date: Older than: ' + args.date + " - " + str(umbralDate) +'\n')
    f.write('Base branch:' + baseBranch + '\n')
    f.write('Report date:' + datetime.today().strftime("%Y-%m-%dT%H:%M:%S%z") +'\n\n')

while fetchAgain:
    # Fetching branches
    url = "https://api.github.com/repos/" + owner +"/"+ repo + "/branches?per_page=100&page=" + str(page) ;
    response = requests.get(url, headers=headers)
    branches = response.json()

    if(response.status_code != 200 ) :
        print('Credentials or connection error')
        exit()
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
                    # To have the array with the names
                    branchesFound.append(br['name'])
                    # Printing info 
                    if br['name'] in protectedBranches:
                        print('\033[94m<Protected>\033[0m')

                    print('Found BRANCH: ' + br['name'])
                    print(' -- Pull Request title: ' + pullRequest['title'] )
                    print(" -- Merged at date: " + pullRequest['merged_at'] + ', to base branch: ' + pullRequest['base']['ref'] +'\n')


                    # BUILDING THE EMAIL STRUCTURE:
                    with open('mails/mail-' + args.reportId + '.txt', 'a') as f:
                        f.write('\033[94m<Protected>\033[0m  \n' if br['name'] in protectedBranches else '')
                        f.write('BRANCH: ' + br['name'] + '\n')
                        f.write(' -- Pull Request title: ' + pullRequest['title'] + '\n')
                        f.write(" -- Merged at date: " + pullRequest['merged_at'] + ', to base branch: ' + pullRequest['base']['ref'] +'\n\n')
    # Checking if we should loop again or we are in the last page     
    if(hasattr(response, 'links')):
        if(not 'last' in response.links) :
            fetchAgain = False;
        page += 1
    else :
        fetchAgain = False;

# Empty results
if(len(branchesFound) <=0 ):
    print('NOT found branches that match the Criteria')
    with open('mails/mail-' + args.reportId + '.txt', 'a') as f:
        f.write('\n\n\n NOT found branches that match the Criteria')

else :       
    # Building json REPORT
    data_set = { "repo" : repo, "branches" : branchesFound}
    json_dump = json.dumps(data_set)
    with open('json-reports/' + args.reportId + ".json", "w") as file:
        file.seek(0)
        json.dump(json_dump, file)

    print("Report JSON ID:"+args.reportId)
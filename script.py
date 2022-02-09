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
parser.add_argument('-p','--protect', default=["main"], nargs='+', dest='protected', help='<Optional> Flag to protect specific branches of being delete by flag --delete-all')
parser.add_argument("--report-id", help="<Optional>  Define the base branch of the search criteria. Default: main", dest='reportId', type=str)

parser.set_defaults(deleteall=False, baseBranch="main")

args = parser.parse_args()

# Getting Token from ENV
token = os.getenv('GITHUB_TOKEN', '...')
# Variables (Maybe convert to ENV)
owner = "marvin-trezlabs"
repo = "GitPracticeRepo"

# Formating date
umbralDate = ''

def convertDate(days):
    global umbralDate
    d = datetime.today() - timedelta(days=days)
    umbralDate = d.strftime("%Y-%m-%dT%H:%M:%S%z")
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

# BUILDING THE EMAIL STRUCTURE: 
# a if for append mode
with open('mail-' + args.reportId + '.txt', 'a') as f:
    f.write('\nOLD BRANCHES REPORT\n')
    f.write('Json ID:' + args.reportId +'\n')
    f.write('Umbral date:' + str(umbralDate) +'\n')
    f.write('Base branch:' + baseBranch)
    f.write('Report date:' + datetime.today().strftime("%Y-%m-%dT%H:%M:%S%z") +'\n')

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


                # BUILDING THE EMAIL STRUCTURE:
                with open('mail-' + args.reportId + '.txt', 'a') as f:
                    f.write('\033[94m<Protected>\033[0m  \n' if br['name'] in protectedBranches else '')
                    f.write('BRANCH: ' + br['name'] + '\n')
                    f.write(' -- Pull Request title: ' + pullRequest['title'] + '\n')
                    f.write(" -- Merged at date: " + pullRequest['merged_at'] + ', to base branch: ' + pullRequest['base']['ref'] +'\n\n')

            if br['name'] not in protectedBranches:
                
                # # Building json
                # with open(umbralDate + '.txt', 'w') as f:
                #     print('Filename:', filename, file=f)
                
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
      # BUILDING THE EMAIL STRUCTURE:
    with open('mail-' + args.reportId + '.txt', 'a') as f:
        f.write('NOT found branches that match the Criteria...')



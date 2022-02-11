import json
import os
import requests
import argparse

parser = argparse.ArgumentParser()
# Defining arguments
# parser.add_argument("--dryrun", help="Set this flag to True to run in safe/report mode", dest='dryrun', action='store_true')
parser.add_argument("--report-id", help="<Optional>  Define the report ID to delete", dest='reportId', type=str)
parser.add_argument("--username", help="Define the Username", dest='username', type=str)

args = parser.parse_args()

# Getting Token from ENV
token = os.getenv('GITHUB_TOKEN', '...')
headers = {'Authorization': f'token {token}'}

# Variables (Maybe convert to ENV)
owner = args.username

jsonObject = {}
with open('json-reports/' + args.reportId + ".json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

print(jsonObject)
repo = jsonObject['repo']
branches = jsonObject['branches']

for data in branches:
    # Deleting the branch
    urlDelete = "https://api.github.com/repos/"+ owner + "/" + repo + "/git/refs/heads/" + data
    responseDelete = requests.delete(urlDelete, headers=headers)
    print('deleting merged branch...')
    if(responseDelete.status_code) :
        print('✔ Deleted successfully')
    else :
        print('✖ Failed to delete')
    break
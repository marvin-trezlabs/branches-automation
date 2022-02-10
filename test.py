from datetime import datetime, timedelta
import argparse
import requests
import os

parser = argparse.ArgumentParser()

parser.add_argument("--date", help="<Required> Date umbral", type=str)
args = parser.parse_args()
token = os.getenv('GITHUB_TOKEN', '...')
headers = {'Authorization': f'token {token}'}

dates = [
'1 week',
'2 weeks',
'1 month',
'3 months',
'1 year',
'2 years',
'All dates'
]
url = "https://api.github.com/repos/marvin-trezlabs/GitPracticeRepo/branches"
response = requests.get(url, headers=headers)
branches = response.json()
print(branches)
umbralDate = ""


def convertDate(days):
    global umbralDate
    d = datetime.today() - timedelta(days=days)
    umbralDate = d.strftime("%Y-%m-%dT%H:%M:%S%z")
    umbralDate = umbralDate + 'Z'
    umbralDate = datetime.strptime(umbralDate, "%Y-%m-%dT%H:%M:%S%z")

if('All dates' == 'All dates'):
    convertDate(0)
else:
    print('ERROR: No matches with that date on loscal array')
    exit()

for br in branches:
    branchName = br['name']
    # Fetching the head commit in order to get the latest commit date
    response2 = requests.get(br['commit']['url'], headers=headers)
    jsondata = response2.json()
    branchDate = jsondata['commit']['author']['date']
    branchDate = datetime.strptime(branchDate, "%Y-%m-%dT%H:%M:%S%z")
    print(branchDate)
    if(branchDate <= umbralDate):
        print('pass the validation')
print(umbralDate)
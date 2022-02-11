# branches-automation


## **Jenkins job:**
---

## Requisites:
- Python3
- Plugins:
  - Active choices, git, cloudbees credentials
- Nodes:
  - Will run on node with label 'linux-node', you can config that on Jenkinsfile
- Workspace:
  - The branch cleaner runs in the 'workspace/branch-cleaner' custom workspace
- Configurations:
  - Github Token credentials
  - SMTP for mails
```
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⣶⣀⣀⣶⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡠⣔⠮⠍⠛⠒⠒⠒⠚⠠⠽⣉⠙⠻⢿⣿⣿⣷⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⡂⠕⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠢⢀⡹⠛⠋⠑⡄⠀⠀⠀
⠀⣀⣀⣠⣼⠏⠀⠀⠀⠀⠀⠀⠀⠜⠑⣄⠀⠀⠀⠀⠀⠠⠊⠀⠀⠀⠀⣷⠀⠀⠀
⣿⣿⣿⣿⡏⠀⠀⠀⢸⠉⢆⠀⠀⢸⣀⣸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡏⠀⠀⠀
⣿⣿⣿⣿⠃⠀⠀⠀⠸⣄⣸⡆⠀⠈⢿⣿⣿⠀⣠⣴⣶⣶⡄⠀⢀⣤⣾⣇⣀⣀⡀
⣿⣿⣿⣿⣦⣄⠀⠀⠀⢻⣿⣿⠀⠀⠈⠻⡿⠀⠘⠛⠛⠋⠁⠸⣿⣿⣿⣿⣿⣿⣿
⣿⣿⡿⢿⣿⣿⣷⢀⣀⠀⠻⠿⢀⣴⣶⣶⡆⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣦⣤⠛⣿⣿⣿⡿⠃⠀⠀⠹⣿⣿⣿⠇⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣦⡈⣿⣿⠇⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃
⠉⠻⣿⣿⣿⣿⣿⣶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀
⠀⠀⠀⠀⠛⢿⣿⣿⣿⣷⢦⣄⣀⡀⠤⣤⣤⣀⣀⣬⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀
⠀⠀⠀⢠⣴⣿⣿⣿⣿⣿⣦⣭⣷⣶⣿⣿⡿⠿⠟⠋⠁⠉⠛⠛⠿⠋⠁
```
TODO:
- THE idea is to have two files: 1 for the mail structure and 1 for the json with the branches names json
- delete every time we send an email the email template file
- Have a checkbox to activate/deactivate the email send
- Read the date param and use the test script for date handling - JUST FIX THE PARSING
- Other jenkins job to delete the branches
- Read the file created from python on the report job
- Build a text box for base branch or remove that parameter


# Script Details:

## Copy config env sample and set a GITHUB token
```
cp example.config.env config.env
```

## Default run script
```bash
bash ./run.sh
```

## Other way to run

Export credentials
```bash
export GITHUB_TOKEN=MyToken
```
Running in dry run mode
```bash
python3 script.py --date=2022-02-05
```

Delete the branches that match the criteria
```bash
python3 script.py --date=2022-02-05 --deleteall
```

If you want to specify a different base branch name, pass the --base-branch flag as follows:
```bash
python3 script.py --date=2022-02-08 --base-branch=master --delete-all
```

Protect branches that you dont want to be deleted even if appears in the Plan / report phase. Default: main
```bash
python3 script.py --date=2022-02-08 --base-branch=main --protect protected_branch other_protected_branch
```
from datetime import datetime, timedelta
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--date", help="<Required> Date umbral", type=str)
args = parser.parse_args()

dates = [
'1 week',
'2 weeks',
'1 month',
'3 months',
'1 year',
'2 years',
'All dates'
]

umbralDate = ""

def convertDate(days):
    global umbralDate
    d = datetime.today() - timedelta(days=days)
    umbralDate = d.strftime("%Y-%m-%dT%H:%M:%S%z")

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
print(umbralDate)
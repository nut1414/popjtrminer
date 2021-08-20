import requests
import time
import json


def fstrclock():
    return f'[{time.strftime("%H:%M:%S",time.gmtime())}]'


print('It is recommended to close all instances of pophq.net before using this.\n')
KEY = str()
while not KEY in ['AC','BC','DS','SK']:
    KEY = input("Enter Team (AC, BC, DS, SK): ")
POPPOWER = int(input("Enter Your Pop Power (MAX 450): "))
DELAY = float(input("Enter Your Delay (between 10-20): ")) # beware of rate limit


urllb = "https://api.pophq.net/leaderboards"
urltk = "https://api.pophq.net/token"



token = ''
if input("Would you like to manually enter token? (y/n) (n if not sure): ") != 'y':
    print(f'{fstrclock()} Getting Token...')
    try:
        token = requests.post(urltk)
        while token.status_code != 200:
            if token.status_code == 429:
                print(f'{fstrclock()} Failed to get token, CODE:{token.status_code} Rate Limit to 2 per 10 minutes, Retrying in 5 minutes...')
            else:
                print(f'{fstrclock()} Failed to get token, CODE:{token.status_code} Retrying in 5 minutes...')
            token = requests.post(urltk)
            time.sleep(303)
    except Exception as error:
        print(f'{fstrclock()} Error: {str(error)}')
    token = json.loads(token.text).get("data")
    print(f"Your token: {token} ")
    tkfile = open('token.txt', 'a')
    tkfile.write(f"{fstrclock()} {token}\n")
    tkfile.close()
else:
    token = input("Enter a token: ")
    tkfile = open('token.txt', 'a')
    tkfile.write(f"{fstrclock()} {token}\n")
    tkfile.close()

print(f'There might be a few rate limit before OK!.')
try:
    reslb = requests.get(urllb)
except Exception as error:
    print(f'{fstrclock()} Error: {str(error)}')

totalpop = 0
keyindex = {"AC":0,"BC":1,"DS":2,"SK":3}.get(KEY,0)

if POPPOWER > 450: # 450 is set limit
    POPPOWER = 450
    print('Capping to 450.')
elif POPPOWER < 0:
    POPPOWER = 0
    print('Capping to 0')


while True:
    time.sleep(DELAY)
    click = POPPOWER
    url = f"https://api.pophq.net/clicks?click={str(click)}&key={KEY}&token={token}"
    
    try:
        res = requests.post(url)
        time.sleep(0.5)

        if res.status_code == 200:
            status = json.loads(res.text)
            success = status.get('success', False)
            pointsadd = status.get('data', {'pointsAdded': 0}).get('pointsAdded')
            if success == True:
                totalpop+=pointsadd
                print(f'{fstrclock()} OK! CODE:{res.status_code}, POP: {pointsadd}, Your Total: {totalpop}, Team Total: {str(json.loads(reslb.text).get("data").get("teams")[keyindex].get("scores"))}')
            else:
                print(f'{fstrclock()} FAIL! CODE:{res.status_code} Error: {status.get("type","unknown_error")}')
        elif res.status_code == 500:
            print(f'{fstrclock()} FAIL! CODE:{res.status_code} Internal Server Error')
        elif res.status_code == 422:
            print(f'{fstrclock()} FAIL! CODE:{res.status_code} Unprocessable Entity')
        else:
            print(f'{fstrclock()} FAIL! CODE:{res.status_code} {json.loads(res.text).get("error")}')
        reslb = requests.get(urllb)
    except Exception as error:
        print(f'{fstrclock()} FAIL! Error: {str(error)}')


import requests
import time
import random
import json

KEY = str()
while not KEY in ['AC','BC','DS','SK']:
    KEY = input("Enter Team (AC, BC, DS, SK): ")
POPPOWER = int(input("Input Your Pop Power (around 100-200 or more): "))

if POPPOWER > 500: # limit for the sanity of the owner?
    POPPOWER = 500
    print('Limiting to 500 for the sanity of the owner.')
elif POPPOWER < 51:
    POPPOWER = 51


POPRANGE = 50
POPMIN = POPPOWER-POPRANGE
POPMAX = POPPOWER+POPRANGE
DELAY = 1 # beware of rate limit
keyindex = {"AC":0,"BC":1,"DS":2,"SK":3}.get(KEY,0)
urllb = "https://popjapi.deta.dev/leaderboards"
print(f'There might be a few rate limit before OK!.')
while(True):
    time.sleep(DELAY)
    click = random.randint(POPMIN,POPMAX)
    url = f"https://popjapi.deta.dev/clicks?click={str(click)}&key={KEY}"
    ftime = f'[{time.strftime("%H:%M:%S",time.gmtime())}]'
    try:
        res = requests.post(url)
        time.sleep(0.5)
        reslb = requests.get(urllb)
        if res.status_code == 200:
            print(f'{ftime} OK! CODE:{res.status_code}, POP: {click}, Team Total: {str(json.loads(reslb.text).get("data").get("teams")[keyindex].get("scores"))}')
        else:
            print(f'{ftime} CODE:{res.status_code} {json.loads(res.text).get("error")}')
    except Exception as error:
        print(f'{ftime} Error: {str(error)}')


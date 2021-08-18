import requests
import time
import random
import json

KEY = "" # AC BC DS SK
POPMIN = 300
POPMAX = 500
DELAY = 1 # beware of rate limit



keyindex = {"AC":0,"BC":1,"DS":2,"SK":3}.get(KEY)
urllb = "https://popjapi.deta.dev/leaderboards"

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
            print(f'{ftime} CODE:{res.status_code} OK, POP: {click}, Team Total: {str(json.loads(reslb.text).get("data").get("teams")[keyindex].get("scores"))}')
        else:
            print(f'{ftime} CODE:{res.status_code} {json.loads(res.text).get("error")}')
    except Exception as error:
        print(f'{ftime} Error: {str(error)}')


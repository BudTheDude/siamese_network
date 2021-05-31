import json
import requests
#headers = {"Authorization": "Bearer ya29.a0AfH6SMCAcHnT7Ht1KZOK08gLRA0m016hbdjpKA1mvR0TT4m0nE6FrYxW85Ovfhe5uHhPoC6a4BC97zFfzFjmIZZBSfOhg1h6aVxpH4qmH08HdlF8PnehaM1N8HcTRBNQxCO62F-mjjA_lnDP-bg-qd4e0zab"}

client_id = "95743473574-u8ij971ddpkln501mp9oph6oho1iuo4i.apps.googleusercontent.com"
client_secret = "xBKQqq2RUsEi4oZRa1uqahCU"
redirect_uri = "https://developers.google.com/oauthplayground"
refresh_token = "1//040DRovhy4m8SCgYIARAAGAQSNwF-L9IrMe_L2iSoXszc8orsrlnOb5CwmapcMLpAyyI9ojbpe2kpBg2Ulrfm-Aj0_WCTU3_ZjbI"
scope = "https://www.googleapis.com/auth/drive"
code = "4/0AY0e-g7J05bZfxd_oqaqO0Mv-BB-7sMCLv5rrm8PUj_58KoFZ1bk-LaC7s3jfeMpxzNE9A"
body = {
      "client_id" : client_id,
      "client_secret" : client_secret,
      "refresh_token": refresh_token,
      "grant_type" : "refresh_token",
    }
token_request = requests.post('https://accounts.google.com/o/oauth2/token',body)
token = token_request.json()["access_token"]




headers = {"Authorization": "Bearer "+ token}

parent_folder="1mFZQ-pYeVD85tHD1Xp3ai3NJwyj-D1OF"

url = "https://www.googleapis.com/drive/v2/files/"+parent_folder+"/children"


r=requests.get(url,headers=headers)

for item in r.json()["items"]:
    url_file = "https://www.googleapis.com/drive/v2/files/"+item["id"]
    r2 = requests.get(url_file,headers=headers)
    
    r3=requests.get(r2.json()["downloadUrl"],headers=headers)
    f = open('myimage.png', 'wb')
    f.write(bytearray(r3.text,encoding='utf8'))
    f.close()
  

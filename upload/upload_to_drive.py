import json
import requests
from datetime import datetime

def upload_image():
    client_id = "95743473574-u8ij971ddpkln501mp9oph6oho1iuo4i.apps.googleusercontent.com"
    client_secret = "xBKQqq2RUsEi4oZRa1uqahCU"
    redirect_uri = "https://developers.google.com/oauthplayground"
    refresh_token = "1//04lg9mjW3LkOdCgYIARAAGAQSNwF-L9IrWKZDmgs_nHwuDi_1VBoE6iE2YxArifEZnlArZH4LFITK2YW5Kx2N-RdWLt9pES5ojhU"
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
    name_now = datetime.now()
    para = {
        "name": str(name_now)+".png",
        "parents":["1mFZQ-pYeVD85tHD1Xp3ai3NJwyj-D1OF"]
    }
    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': open("./sexy.png", "rb")
    }
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files
    )
    print(r.text)
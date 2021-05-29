import json
import requests
headers = {"Authorization": "Bearer ya29.a0AfH6SMCAcHnT7Ht1KZOK08gLRA0m016hbdjpKA1mvR0TT4m0nE6FrYxW85Ovfhe5uHhPoC6a4BC97zFfzFjmIZZBSfOhg1h6aVxpH4qmH08HdlF8PnehaM1N8HcTRBNQxCO62F-mjjA_lnDP-bg-qd4e0zab"}
para = {
    "parents":["1mFZQ-pYeVD85tHD1Xp3ai3NJwyj-D1OF"]
}

GET https://www.googleapis.com/drive/v3/files

r=requests.get("https://www.googleapis.com/drive/v3/files",headers=headers)

print(r.text)

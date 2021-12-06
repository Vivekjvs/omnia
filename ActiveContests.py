import json
import requests

def getActiveContests():
    ClistURL = "https://clist.by/api/v2/contest/?username=srikar23&api_key=26da379142f75b94ef2ba1a6bd5de9379f69f47c&format=json"
    req = requests.get(ClistURL)
    req.raise_for_status()  # raises exception when not a 2xx response
    jsonData =[]
    if req.status_code != 204:
        jsonData = req.json()["objects"]

    Contestdict = {"hackerrank.com":[],"codechef.com":[],"codeforces.com":[],"hackerearth.com":[],"leetcode.com":[],"spoj.com":[]}
    for currContest in jsonData:
        platform = currContest["host"]
        if platform in Contestdict:
            Contestdict[platform].append(currContest)
    return Contestdict

getActiveContests()
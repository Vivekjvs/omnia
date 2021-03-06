from datetime import date

from itsdangerous import exc
from AdminDatabase import *
import requests
import json

def getCodeforcesRating(codeforcesHandle):
    try:
        profileUrl = f"https://competitive-coding-api.herokuapp.com/api/codeforces/{codeforcesHandle}"
        req = requests.get(profileUrl)
        jsonData = json.loads(req.content)

        rating = int(jsonData['rating'])

        req.close()
        return int(rating)
    except:
        return 0

def getCodechefRating(codechefHandle):
    try:
        profileUrl = f"https://competitive-coding-api.herokuapp.com/api/codechef/{codechefHandle}"
        req = requests.get(profileUrl)
        jsonData = json.loads(req.content)
        #print(jsonData)

        rating = int(jsonData['rating'])
        rating = (((rating-1300)**2)//30)

        totalsolved = int(jsonData["fully_solved"]["count"])
        rating = rating + totalsolved*20

        req.close()
        return rating
    except:
        return 0
    

def getInterviewBitRating(inerviewbitHandle):
    try:
        profileUrl = f"https://competitive-coding-api.herokuapp.com/api/interviewbit/{inerviewbitHandle}"
        req = requests.get(profileUrl)
        jsonData = json.loads(req.content)
        score = int(jsonData["score"])
        req.close()
        return score//10
    except:
        return 0
    

def getSpojRating(spojHandle):
    try:
        profileUrl = f"https://competitive-coding-api.herokuapp.com/api/spoj/{spojHandle}"
        req = requests.get(profileUrl)
        jsonData = json.loads(req.content)
        points = float(jsonData["points"])
        submissions = len(jsonData["solved"])

        rating = points*500+submissions*10
        req.close()
        return int(rating)
    except:
        return 0
    
def getLeetcodeRating(leetcodeHandle):
    try:    
        profileUrl = f"https://competitive-coding-api.herokuapp.com/api/leetcode/{leetcodeHandle}"
        req = requests.get(profileUrl)
        jsonData = json.loads(req.content)

        totalProblemsSolved = int(jsonData["total_problems_solved"])

        contributionPoints = int(jsonData["contribution_points"])

        rating = contributionPoints + totalProblemsSolved*10
        req.close()
        return int(rating)
    except:
        return 0
    
def getOverAllRating(codeforcesRating,codechefRating,interviewBitRating,spojRating,leetcodeRating):
    return sum([codeforcesRating,codechefRating,interviewBitRating,spojRating,leetcodeRating])


def updateScore():
    #gathering all the registered userIds
    users = getAllUsers()

    for user in users:
        userId = user[0]
        handles = getUserHandles(userId)
        if(handles is None):
            print("The user does not exists")
            exit(0)

        #retrivng the scores of all platforms
        codechefRating = getCodechefRating(handles["codechef"])
        codeforcesRating = getCodeforcesRating(handles["codeforces"])
        interviewBitRating = getInterviewBitRating(handles["interviewBit"])
        leetcodeRating = getLeetcodeRating(handles["leetcode"])
        spojRating = getSpojRating(handles["spoj"])

        #calculating overall score
        overAllRating = getOverAllRating(codeforcesRating,codechefRating,interviewBitRating,spojRating,leetcodeRating)

        currentDate = date.today().strftime("%Y-%m-%d")
        
        #to update the values in the database table
        updateLeaderBoard(userId,codechefRating,codeforcesRating,interviewBitRating,leetcodeRating,spojRating,overAllRating,currentDate)
        
if __name__ == "__main__":
    updateScore()
    
import json
import requests
from CodeforcesDatabase import addToContestDetails,addToProblemDetails

def updateAllContestDetails():
    #using This API we get all contests that were hosted by codeforces
    codeforcesContestLink = f'https://codeforces.com/api/contest.list'
    req = requests.get(codeforcesContestLink)
    jsonData = json.loads(req.content)["result"]

    #Iterating over each contest of codeforces
    for currContest in jsonData:
        contestId = currContest["id"]
        contestName = currContest["name"]
        contestStartTime = currContest["startTimeSeconds"]

        #Adding contest details to database Table
        #Method is in CodeforcesDatabase.py
        addToContestDetails("codeforces"+str(contestId),contestName,contestStartTime)
    
    #print("updateAllContestDetails: All the contest details of codeforces are updated")

def updateAllProblemDetails():

    #using This API we get all problems present in codeforces
    codeforcesProblemLink = f'https://codeforces.com/api/problemset.problems'
    req = requests.get(codeforcesProblemLink)
    jsonData = json.loads(req.content)["result"]["problems"]

    #Iterating over each problem in codeforces
    for currProblem in jsonData:
        contestId = currProblem["contestId"]
        Index = currProblem["index"]
        problemId = str(contestId)+Index
        problemName = currProblem["name"]
        problemLink = f'https://codeforces.com/problemset/problem/{contestId}/{Index}'

        #Adding problem details to database Table
        #Method is in CodeforcesDatabase.py
        addToProblemDetails(problemId,problemName,problemLink)
    #print("updateAllProblemDetails: All the problem details of codeforces are updated")

def updateCodeforcesProblems_Contests():
    try:
        #To update details of all problems available in codeforces into the database
        updateAllProblemDetails()

        #To update details of all contests available in codeforces into the database
        updateAllContestDetails()
    except:
        print("Error in codeforces problems_ContestDetails File")

if __name__ == "__main__":
    updateCodeforcesProblems_Contests()
    
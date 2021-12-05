import json
from CodeforcesDatabase import *
import requests
from bs4 import BeautifulSoup
from AdminDatabase import getUserHandles

problemSet = {}
#To store the count of each verdict for Piechart in our website
submissionCount = {"TimeLimitExceedCount":0,"CompileTimeErrorCount":0,"WrongAnswerCount":0,"RuntimeErrorCount":0,"AcceptedCount":0}


def updateSubmissionCount(problemName,verdict):
    #updating the count of respective verdict for data analysis
    if(verdict[0] =="A"):
        #to ignore the accepted verdict for same problem
        try:
            if(problemSet[problemName] == 1):
                return            
        except:
            problemSet[problemName] = 1
            submissionCount["AcceptedCount"] += 1
    elif(verdict[0] =="T"):
        submissionCount["TimeLimitExceedCount"] += 1
    elif(verdict[0] =="R"):
        submissionCount["RuntimeErrorCount"] += 1
    elif(verdict[0] =="W"):
        submissionCount["WrongAnswerCount"] += 1
    elif(verdict[0] =="C"):
        submissionCount["CompileTimeErrorCount"] += 1

def updateUserProblemDetails(userid,codeforcesHandle):

    jsonData = ""
    try:
        #using the API we will get all the submissions of particular handle
        codeforcesStatusPage = f"https://codeforces.com/api/user.status?handle={codeforcesHandle}"
        req = requests.get(codeforcesStatusPage)
        #formatting into json data
        jsonData = json.loads(req.content)["result"]
    except Exception as e:
        print("Exception Message(updateUserProblemDetails):",e)
        return 
    #Main tags we have in programming
    totalTags = ["binarySearch","binaryTree","matrices","arrays","probabilities","implementation","math","backtracking","numberTheory","divideAndConquer","bruteforce","dp","graphs","trees","dfs","bfs","bitManipulation","strings","dataStructures","games","greedy","hashing","sorting","twopointers","Others"]
    
    #Here each problem is stored with its respective tags as true
    for currentProblem in jsonData:
        contestId = currentProblem["problem"]["contestId"]
        contestIndex = currentProblem["problem"]["index"]
        tags = currentProblem["problem"]["tags"]
        problemName = currentProblem["problem"]["name"]
        verdict = currentProblem["verdict"]
        if verdict=="OK":
            verdict = "ACCEPTED" 

        problemId = str(contestId)+str(contestIndex)

        currProblem = {}
        currProblem["userId"] = userid
        currProblem["problemId"] = problemId
        currProblem["verdict"] = verdict
        for tag in totalTags:
            currProblem[tag] = False
        
        for tag in tags:
            if tag == "binary search":
                currProblem["binarySearch"] = True
            elif tag == "bitmasks":
                currProblem["bitManipulation"] = True
            elif tag == "brute force":
                currProblem["bruteforce"] = True
            elif tag == "data structures":
                currProblem["dataStructures"] = True
            elif tag == "dfs and similar":
                currProblem["dfs"] = True
            elif tag == "dp":
                currProblem["dp"] = True
            elif tag == "games":
                currProblem["games"] = True
            elif tag == "graph matchings" or tag == "graphs":
                currProblem["graphs"] = True
            elif tag == "greedy":
                currProblem["greedy"] = True
            elif tag == "hashing":
                currProblem["hashing"] = True
            elif tag == "implementation":
                currProblem["implementation"] = True
            elif tag == "math":
                currProblem["math"] = True
            elif tag == "matrices":
                currProblem["matrices"] = True
            elif tag == "number theory":
                currProblem["numberTheory"] = True
            elif tag == "probabilities":
                currProblem["probabilities"] = True
            elif tag == "sortings":
                currProblem["sorting"] = True
            elif tag == "string suffix structures" or tag == "strings":
                currProblem["strings"] = True
            elif tag == "trees":
                currProblem["trees"] = True
            elif tag == "two pointers":
                currProblem["twopointers"] = True
            elif tag == "divide and conquer":
                currProblem["divideAndConquer"] = True
            else:
                currProblem["Others"] = True
        
        #To add the problem details into database
        #Method available in CodeforcesDatabase.py file
        addToUserProblemDetails(list(currProblem.values()))

        #updating the count of each verdict for piechart
        updateSubmissionCount(problemName,verdict)
    print("updateUserSubmissionDetails: All the problems are inserted")

def updateUserContestDetails(userid,codeforcesHandle):
    #By using this API we get all the contest details in which particular user participated
    req = ""
    try:
        codeforcesProfile = f'https://codeforces.com/api/user.rating?handle={codeforcesHandle}'
        req = requests.get(codeforcesProfile)
    except Exception as e:
        print("Exception Message(updateUserContestDetails):",e)
        return
    #converting to json format for easy usage
    jsonData = json.loads(req.content)["result"]

    #iterating over all the contests that user participated
    for currContest in jsonData:
        contestId = "codeforces"+str(currContest["contestId"])
        oldRating = currContest["oldRating"]
        newRating = currContest["newRating"]
        contestRating = newRating-oldRating
        contestRank = currContest["rank"]

        #to insert the values into database
        #Method available in CodeforcesDatabase.py file
        addToUserContestDetails(userid,"codeforces",contestId,contestRank,contestRating,newRating)

    print("userContestDetails: All user contest details of codeforces are updated")


def main(userid):

    #Taking userId of our website 

    codeforcesHandle = ""
    try:
        #Retriving 
        codeforcesHandle = getUserHandles(userid)["codeforces"]
    except:
        print("Enter valid userId")
        exit(0)

    codeforcesProfile = f'https://codeforces.com/profile/{codeforcesHandle}'
    req = requests.get(codeforcesProfile)
    soup = BeautifulSoup(req.content,"html5lib")

    try:
        div_info = soup.find('div',class_ = 'info')
        #scraping the rating of user from webpage
        rating = div_info.ul.li.span.text
    except:
        print("Please enter a valid codefrces Handle")
        exit(0)


    print("Details of",codeforcesHandle,":")
    print("Current Rating:",rating)

    #total no.of problems solved by the user
    no_of_problems = int(soup.find('div',class_ ='_UserActivityFrame_counterValue').text.split(" ")[0])
    print("Total no of problems solved till now:",no_of_problems,"\n")

    #Methods to update particular user details in the database
    updateUserContestDetails(userid,codeforcesHandle)

    updateUserProblemDetails(userid,codeforcesHandle)

    #Finally adding the count of each verdict to the database
    #Method available in CodeforcesDatabase.py
    addToSubmissionsInDb(userid,submissionCount)
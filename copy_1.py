import requests
import creds
import time

'''Get Requests'''

def get_OgranisationRepos(organisation_name):

    url = "https://api.github.com/orgs/{org}/repos?per_page=100&page={pag}"

    headers = {"Authorization": 'token ' + creds.api_key , }

    all_results = []
    page = 1
    while True:
        response = requests.get(url.format(org=organisation_name,pag=page), headers=headers).json()
        if len(response) == 0:
            break
        all_results.extend(response)
        page += 1

    return all_results

def get_UserRepo(user_name,repo_name):

    url = "https://api.github.com/repos/{owner}/{repo}"
    headers = {"Authorization": 'token ' + creds.api_key}

    response = requests.get(url.format(owner=user_name, repo=repo_name), headers=headers).json()

    return response

def get_RepoIssues(user_name,repo_name):

    url = "https://api.github.com/repos/{owner}/{repo}/issues?per_page=100&page={pag}"
    headers = {"Authorization": 'token ' + creds.api_key}

    all_results = []
    page = 1
    while True:
        response = requests.get(url.format(owner=user_name, repo=repo_name,pag=page), headers=headers).json()
        if len(response) == 0:
            break
        all_results.extend(response)
        page += 1

    return all_results

def get_RepoMilestones(user_name,repo_name):

    url = "https://api.github.com/repos/{owner}/{repo}/milestones?per_page=100&page={pag}"
    headers = {"Authorization": 'token ' + creds.api_key}

    all_results = []
    page = 1
    while True:
        response = requests.get(url.format(owner=user_name, repo=repo_name,pag=page), headers=headers).json()
        if len(response) == 0:
            break
        all_results.extend(response)
        page += 1

    return all_results


'''Check for existing Elements'''

def check_MilestoneExist(exist_milestones,milestone):


    for exist_milestone in exist_milestones:
        flag = exist_milestone['title']==milestone['title'] and exist_milestone['description']==milestone['description']
        if(flag):
            return True
  
    return False

def check_IssueExist(exist_issues,issue):


    for exist_issue in exist_issues:
        flag = exist_issue['title']==issue['title'] and exist_issue['body']==issue['body']
        if(flag):
            return True
  
    return False

def check_IssueExistMilestone(exist_issues,issue):


    for exist_issue in exist_issues:
        flag_1 = exist_issue['milestone']['title']==issue['milestone']['title'] and exist_issue['milestone']['description']==issue['milestone']['description']
        flag_2 = exist_issue['title']==issue['title'] and exist_issue['body']==issue['body']
        
        if(flag_1 and flag_2):
            return True
  
    return False

'''Post Request'''

def post_RepoMilestones(user_name,repo_name,milestones):

    url = "https://api.github.com/repos/{owner}/{repo}/milestones"
    headers = {"Authorization": 'token ' + creds.api_key}
    
    exist_milestones = get_RepoMilestones(user_name,repo_name)



    for milestone in milestones:

        '''When a milestone with the same tite and bod exist it will not be posted'''
        if(check_MilestoneExist(exist_milestones,milestone)):
            continue
        
        
        data = {
            "title": milestone['title'],
            "state": milestone['state'],
            "description": milestone['description'],
            "due_on": milestone.get('due_on')
            
        }

        response = requests.post(url.format(owner=user_name, repo=repo_name), headers=headers, json=data)
        #print(response.json())


def post_RepoIssues(user_name, repo_name, issues):
    url = "https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {"Authorization": 'token ' + creds.api_key,'User-Agent': 'request'}
    
    exist_milestones = get_RepoMilestones(user_name,repo_name)
    exist_issues = get_RepoIssues(user_name,repo_name)

    for issue in issues:

        '''When a issue exist AND the issue is assigned to the same milestone 
        it will not be posted'''
        if(check_IssueExistMilestone(exist_issues,issue)):
            continue
            

        for milestone in exist_milestones:
            if(milestone['title']==issue['milestone']['title']):
                number = milestone['number']

        data = {
            "owner": user_name,
            "user": issue['user'],
            "title": issue['title'],
            "state": issue['state'],
            "body": issue['body'],
            "labels": issue['labels'],
            "milestone": number

            #"due_on": milestone['due_on']
        }

        response = requests.post(url.format(owner=user_name, repo=repo_name), headers=headers, json=data)
        if(response.status_code != 201):
            print("Issue: {}".format(issue['title']))
            print("Statuscode: {}".format(response.status_code))
            print(response.json())
            return response.status_code



def main():
    #Get requests
    user_name ="AI-Assistant" 
    organisation_name = "GSO-SW"
    user_repo = "ELearning"
    org_repo_get = "BFT31MultiTool"

    #Post requests
    org_repo_post = "BFT32MultiTool"



    #Testing to get information
    #org_repositorys = get_OgranisationRepos(organisation_name).json()
    #spec_repo = get_UserRepo(organisation_name,org_repo).json()
    
    #1. First copy the milestones (Check if the milestone exist after copying)
    # spec_repo_milestones = get_RepoMilestones(organisation_name,org_repo_get)
    # post_RepoMilestones(organisation_name,org_repo_post,spec_repo_milestones)
    
    #2. Then copy the issues
    #Due to limitations of GitHub API, the script runs multiple times to copy all issues (script will not copy issues with the same title, body and milestone)
    #Github API allows only limited number of requests per hour so you have to wait for a while when you got many issues
    spec_repo_issues = get_RepoIssues(organisation_name,org_repo_get)
    
    status_code = 0

    while True:

        status_code =post_RepoIssues(organisation_name,org_repo_post,spec_repo_issues)
        if(status_code==403):
            time.sleep(100)
        else:
            break









if __name__ == "__main__":

    main()





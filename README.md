# GitHub Repository Management Tool

## Overview
This Python tool is designed to manage GitHub repositories within an organization. It automates the process of copying milestones and issues from one repository to another within the same organization. This is particularly useful for maintaining consistency across different projects within an organization.

## Features
- **Get Organization Repositories**: Fetches all repositories under a specific organization.
- **Get User Repository**: Retrieves a specific repository's details.
- **Get Repository Issues and Milestones**: Collects all issues and milestones associated with a specific repository.
- **Check for Existing Elements**: Checks for the existence of milestones and issues to avoid duplication.
- **Post Requests**: Ability to post new milestones and issues to a repository.

## Installation

Before you begin, ensure you have Python installed on your machine. Then, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/AI-Assistant/issue_copy.git)https://github.com/AI-Assistant/issue_copy.git
```
2. Navigate to the project directory:   
```bash
cd [PROJECT_DIRECTORY]
```
3. Install required packages:   
```bash
pip install virtualenv
```

Create virtual enviorment:   
```bash
virtualenv venv
```

Activate virtual enviorment:   
```bash
.\venv\Scripts\activate
```

Install requirements:   
```bash
pip install -r requirements.txt
```
## Usage

1. Set up your GitHub API credentials in a **creds.py** file:

```python
api_key = "YOUR_GITHUB_API_KEY"
```

2. Edit the **'main'** function in the script to specify the source and target repositories for copying milestones and issues.
```python
#Get requests
organisation_name = "ORGANISATION" #Name of the organisation
org_repo_get = "RepoWithIssues" #Name of the repository to copy from

#Post requests
org_repo_post = "RepoWithoutIssues" #Name of the repository to copy to
```
3. Run the script.

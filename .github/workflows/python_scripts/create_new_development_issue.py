import os
import json
import requests

# Get data from past steps
base_game = os.environ['BASE_GAME']
implementer = os.environ['IMPLEMENTER']
description = os.environ['DESCRIPTION']
issue_author = os.environ['ISSUE_AUTHOR']

# Initialize GitHub API data
repo = os.environ['GITHUB_REPOSITORY']
token = os.environ['GITHUB_TOKEN']
headers = {
  'Authorization': f'token {token}',
  'Accept': 'application/vnd.github.v3+json'
}

# Prepare issue data
title = f"[PATCH DEVELOPMENT]: {base_game}: {description}"
body = f"**Original Suggestion:** #{os.environ['ORIGINAL_ISSUE_NUMBER']}\n\n"
assignee = issue_author if implementer == 'I will develop it myself' else 'PurnPum'

# Create new issue
response = requests.post(
  f"https://api.github.com/repos/{repo}/issues",
  headers=headers,
  json={
    'title': title,
    'body': body,
    'labels': ['patch development'],
    'assignees': [assignee]
  }
)

# Output the new issue number
new_issue = response.json()
with open(os.environ['GITHUB_OUTPUT'], 'a') as output_file:
  output_file.write(f'issue_number={new_issue['number']}\n')
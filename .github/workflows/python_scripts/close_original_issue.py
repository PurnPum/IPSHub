import requests
import os

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
REPOSITORY = os.environ['GITHUB_REPOSITORY']
ISSUE_NUMBER = os.environ['ORIGINAL_ISSUE_NUMBER']
NEW_ISSUE_NUMBER = os.environ['ISSUE_NUMBER']
GITHUB_API_URL = f"https://api.github.com/repos/{REPOSITORY}/issues/{ISSUE_NUMBER}"

headers = {
  "Authorization": f"token {GITHUB_TOKEN}",
  "Accept": "application/vnd.github.v3+json"
}

def close_issue():
  data = {
    "state": "closed"
  }
    
  response = requests.patch(GITHUB_API_URL, headers=headers, json=data)
    
  if response.status_code == 200:
    print(f"Issue #{ISSUE_NUMBER} closed successfully.")
  else:
    print(f"Failed to close the issue #{ISSUE_NUMBER}. Response: {response.content}")

def post_comment():
  comment_url = f"{GITHUB_API_URL}/comments"
  comment_data = {
    "body": f"This issue has been approved and resolved. See the development progress at issue #{NEW_ISSUE_NUMBER}."
  }

  response = requests.post(comment_url, headers=headers, json=comment_data)

  if response.status_code == 201:
    print(f"Comment posted successfully on issue #{ISSUE_NUMBER}.")
  else:
    print(f"Failed to post comment on issue #{ISSUE_NUMBER}. Response: {response.content}")

# Call the functions
close_issue()
post_comment()

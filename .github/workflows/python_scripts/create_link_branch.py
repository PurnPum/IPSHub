import requests
import sys, os

def create_branch():
    
  branchName = f"patchdev/{ISSUE_ID:04d}"
  payload = {
    "name": branchName,
    "branch": "main",
    "after_create": "checkout-locally",
    "skip_error_flash": "true",
  }

  response = requests.post(GITHUB_API_URL_LINK_BRANCH, json=payload, headers=headers)

  if response.status_code == 200:
    print(f"Branch {branchName} created successfully!")
  else:
    print(f"Failed to create branch {branchName}. Status code: {response.status_code}")
    print(response.json())
    sys.exit(1)
    
if __name__ == '__main__':
  ISSUE_ID = os.environ['ISSUE_ID']
  REPOSITORY = os.environ['GITHUB_REPOSITORY']
  GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
  GITHUB_API_URL_LINK_BRANCH = f"https://github.com/{REPOSITORY}/issues/{ISSUE_ID}/branch"
  
  headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
  }
    
  create_branch()
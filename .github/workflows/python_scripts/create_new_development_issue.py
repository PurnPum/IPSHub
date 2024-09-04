import os
import re
import sys
import requests

def close_issue():
  data = {
    "state": "closed"
  }
    
  response = requests.patch(GITHUB_API_URL_ISSUENUM, headers=headers, json=data)
    
  if response.status_code == 200:
    print(f"Issue #{ISSUE_NUMBER} closed successfully.")
  else:
    print(f"Failed to close the issue #{ISSUE_NUMBER}. Response: {response.content}")
    sys.exit(1)
  return response

def post_comment(new_issue_num,user_developed=True):
  comment_url = f"{GITHUB_API_URL_ISSUENUM}/comments"
  if user_developed:
    pass # TODO extra_comment
  comment_data = {
    "body": f"This issue has been approved and resolved. See the development progress at issue #{new_issue_num}."
  }

  response = requests.post(comment_url, headers=headers, json=comment_data)

  if response.status_code == 201:
    print(f"Comment posted successfully on issue #{ISSUE_NUMBER}.")
  else:
    print(f"Failed to post comment on issue #{ISSUE_NUMBER}. Response: {response.content}")
    sys.exit(1)

def parse_issue_form_data():
  body = os.environ['ISSUE_BODY']
  title = os.environ['ISSUE_TITLE']

  # Extract data from the issue body
  body_pattern = r"(### Suggestion Details.*)(### Base Game\n\n)(.*)(\n\n)(### Implementer\n\n)(.*)"
  title_pattern = r"^(.*)(:[\s*])(.*)"

  base_game = re.search(body_pattern,body,re.DOTALL).group(3)
  implementer = re.search(body_pattern,body,re.DOTALL).group(6)
  description = re.search(title_pattern,title).group(3)
  
  return {'base_game': base_game, 'implementer': implementer, 'description': description}

def create_issue(base_game, implementer, description):

  title = f"[PATCH DEVELOPMENT]: {base_game}: {description}"
  body = f"**Original Suggestion:** #{ISSUE_NUMBER}\n\n"
  assignee = ISSUE_AUTHOR if implementer == 'I will develop it myself' else 'PurnPum'

  response = requests.post(
    GITHUB_API_URL_ISSUES,
    headers=headers,
    json={
      'title': title,
      'body': body,
      'labels': ['patching/development'],
      'assignees': [assignee]
    }
  )

  try:
    new_issue = response.json()
    post_comment(new_issue['number'],user_developed = implementer == 'I will develop it myself')
    # TODO Add team/user label
    with open(os.environ['GITHUB_ENV'], 'a') as env_file:
      issue_id = new_issue['number']
      env_file.write(f"issue_id={issue_id}\n")
  except:
    print(f"Failed to create issue. Response: {response.content}")
    sys.exit(1)

if __name__ == '__main__':
  GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
  REPOSITORY = os.environ['GITHUB_REPOSITORY']
  ISSUE_NUMBER = os.environ['ORIGINAL_ISSUE_NUMBER']
  ISSUE_AUTHOR = os.environ['ISSUE_AUTHOR']
  GITHUB_API_URL_ISSUENUM = f"https://api.github.com/repos/{REPOSITORY}/issues/{ISSUE_NUMBER}"
  GITHUB_API_URL_ISSUES = f"https://api.github.com/repos/{REPOSITORY}/issues"
  GITHUB_API_URL_REFS = f"https://api.github.com/repos/{REPOSITORY}/git/refs"

  headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
  }
  data = parse_issue_form_data()
  number = create_issue(data['base_game'], data['implementer'], data['description'])
  close_issue()
  
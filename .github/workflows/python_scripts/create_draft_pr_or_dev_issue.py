import os
import re
import sys
import requests

def post_comment(comment_url, comment_data):
  response = requests.post(comment_url, headers=headers, json=comment_data)

  if response.status_code == 201:
    print(f"Comment posted successfully.")
  else:
    print(f"Failed to post comment. Response: {response.content}")
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

def create_issue(base_game, description):
  new_branch = create_branch(ISSUE_NUMBER)
  title = f"[PATCH DEVELOPMENT]: {base_game}: {description}"
  body = f"**Original Suggestion:** #{ISSUE_NUMBER}\n\n**Created branch:** [{new_branch}](https://github.com/{REPOSITORY}/tree/{new_branch})"
  base_game_label = BASE_GAME_LABELS[base_game]
  try:
    response = requests.post(
      GITHUB_API_ISSUES,
      headers=headers,
      json={
        'title': title,
        'body': body,
        'labels': ['patching/development', f"base_game/{base_game_label}", 'patching/user-developed'],
        'assignees': [ISSUE_AUTHOR],
      }
    )

    new_issue = response.json()
    return new_issue['number']
  except:
    print(f"Failed to create issue. Response: {response.content}")
    sys.exit(1)

def create_draft_pr(base_game):
  base_game_label = BASE_GAME_LABELS[base_game]
  new_branch = create_branch(ISSUE_NUMBER)
  try:
    response = requests.post(
      GITHUB_API_PULLS,
      headers=headers,
      json={
        'issue': int(ISSUE_NUMBER),
        'draft': True,
        'labels': ['patching/pull-request', f"base_game/{base_game_label}", 'patching/team-developed'],
        'assignees': [ISSUE_AUTHOR],
        'base': 'patch_implementations',
        'head': new_branch,
      }
    )
    new_pr = response.json()
    return new_pr['number']
  except:
    print(f"Failed to create PR. Response: {response.content}")
    sys.exit(1)

def close_issue():
  data = {
    "state": "closed"
  }
    
  response = requests.patch(GITHUB_API_ISSUENUM, headers=headers, json=data)
    
  if response.status_code == 200:
    print(f"Issue #{ISSUE_NUMBER} closed successfully.")
  else:
    print(f"Failed to close the issue #{ISSUE_NUMBER}. Response: {response.content}")
    sys.exit(1)
  return response

def create_branch(issue_id):
  branchName = f"patchdev/{int(issue_id):04d}"
  
  response = requests.get(GITHUB_API_BRANCH, headers=headers)

  if response.status_code == 200:
    latest_commit_sha = response.json()["object"]["sha"]
    print(f"Latest commit SHA for {BASE_BRANCH}: {latest_commit_sha}")
  else:
    print(f"Failed to get base branch: {response.content}")
    exit(1)

  data = {
    "ref": f"refs/heads/{branchName}",
    "sha": latest_commit_sha
  }
  response = requests.post(GITHUB_API_REFS, headers=headers, json=data)

  if response.status_code == 201:
    print(f"Branch '{branchName}' created successfully.")
  else:
    print(f"Failed to create branch: {response.content}")
    sys.exit(1)
  return branchName

if __name__ == '__main__':
  GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
  REPOSITORY = os.environ['GITHUB_REPOSITORY']
  ISSUE_NUMBER = os.environ['ORIGINAL_ISSUE_URL'].split('/')[-1]
  ISSUE_AUTHOR = os.environ['ISSUE_AUTHOR']
  BASE_BRANCH = 'patch_implementations'
  GITHUB_API = f"https://api.github.com/repos/{REPOSITORY}"
  GITHUB_API_REFS = f"{GITHUB_API}/git/refs"
  GITHUB_API_BRANCH = f"{GITHUB_API_REFS}/heads/{BASE_BRANCH}"
  GITHUB_API_ISSUES = f"{GITHUB_API}/issues"
  GITHUB_API_ISSUENUM = f"{GITHUB_API_ISSUES}/{ISSUE_NUMBER}"
  GITHUB_API_PULLS = f"{GITHUB_API}/pulls"
  BASE_GAME_LABELS = {"Pokémon: Yellow Edition": "pokeyellow", "Pokémon: Crystal Edition": 'pokecrystal'}

  headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
  }
  data = parse_issue_form_data()
  if data['implementer'] == 'I will develop it myself':
    new_issue_id = create_issue(data['base_game'], data['description'])
    comment_url = f"{GITHUB_API_ISSUENUM}/comments"
    comment_data = {
      "body": f"This suggestion has been approved. The development process has been moved to issue #{new_issue_id}."
    }
    post_comment(comment_url, comment_data)
    close_issue()
  else:
    new_issue_id = create_draft_pr(data['base_game'])
    comment_url = f"{GITHUB_API_ISSUES}/{new_issue_id}/comments"
    comment_data = {
      "body": f"This suggestion has been approved. The development process has been moved to the following pull request: #{new_issue_id}."
    }
    post_comment(comment_url, comment_data)
  
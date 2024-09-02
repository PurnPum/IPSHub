import os
from github import Github

# Initialize GitHub client
g = Github(os.environ['GITHUB_TOKEN'])
repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
issue_number = os.environ['GITHUB_EVENT_ISSUE_NUMBER']
issue = repo.get_issue(int(issue_number))

# Output issue data
with open(os.environ['GITHUB_OUTPUT'], 'a') as output_file:
  output_file.write(f'issue_data={issue.raw_data}\n')
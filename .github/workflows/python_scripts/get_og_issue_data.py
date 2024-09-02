import os
from github import Github

# Initialize GitHub client
g = Github(os.environ['GITHUB_TOKEN'])
repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
issue_url = os.environ['ORIGINAL_ISSUE']
issue_number = issue_url.split("/")[-1]
issue = repo.get_issue(int(issue_number))

# Output issue data
with open(os.environ['GITHUB_OUTPUT'], 'a') as output_file:
  output_file.write(f'issue_data={issue.raw_data}\n')
  output_file.write(f'original_issue_number={issue_number}\n')
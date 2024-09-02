import json
import re
import os

# Load issue data from the previous step's output
issue_data = json.loads(os.environ['ISSUE_DATA'])
body = issue_data['body']
title = body['title']
user_login = body['user']['login']

# Extract data from the issue body
base_game = issue_data['base_game']
implementer = issue_data['implementer']
description = re.search(r"^(.*)(:[\s*])(.*)",title).group(3)

# Set outputs for the next steps
with open(os.environ['GITHUB_OUTPUT'], 'a') as output_file:
  output_file.write(f'base_game={base_game}\n')
  output_file.write(f'implementer={implementer}\n')
  output_file.write(f'description={description}\n')
  output_file.write(f'issue_author={user_login}\n')
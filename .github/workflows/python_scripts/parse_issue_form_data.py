import re
import os

body = os.environ['ISSUE_BODY']
title = os.environ['ISSUE_TITLE']
print("body: " + body, "title: " + title)

# Extract data from the issue body
body_pattern = r"(### Suggestion Details.*)(### Base Game\n\n)(.*)(\n\n)(### Implementer\n\n)(.*)"
title_pattern = r"^(.*)(:[\s*])(.*)"

base_game = re.search(body_pattern,body,re.DOTALL).group(3)
implementer = re.search(body_pattern,body,re.DOTALL).group(6)
description = re.search(title_pattern,title).group(3)
print("base_game: " + base_game, "implementer: " + implementer, "description: " + description)

# Set outputs for the next steps
with open(os.environ['GITHUB_OUTPUT'], 'a') as output_file:
  output_file.write(f'base_game={base_game}\n')
  output_file.write(f'implementer={implementer}\n')
  output_file.write(f'description={description}\n')
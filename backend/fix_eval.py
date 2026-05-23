import re

with open('tests/eval_data.py', 'r') as f:
    content = f.read()

# find all "Complex Boolean Condition" blocks
blocks = re.findall(r'    \{\n        "name": "Complex Boolean Condition".*?\n    \},?\n', content, re.DOTALL)

for block in blocks:
    if 'and e and f' not in block:
        content = content.replace(block, '')

with open('tests/eval_data.py', 'w') as f:
    f.write(content)

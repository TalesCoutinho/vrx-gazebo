import os
def get_workspace_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.abspath(__file__))

import re

with open(os.path.join(get_workspace_root(), 'vrx/vrx_gz/worlds/bathymetry.sdf'), 'r') as f:
    content = f.read()

# Pattern to match strictly the include blocks for buoys without grabbing other includes
pattern = r"<include>[\s]*<name>mb_[^<]+</name>.*?<\/include>"
# re.sub with DOTALL will match across newlines, but we must be careful with .*?
# A better regex is:
# <include>\s*(?:<pose>[^<]+</pose>\s*)?<name>mb_[^<]+</name>[\s\S]*?</include>

pattern = r"<include>\s*(?:<pose>[^<]*</pose>\s*)?<name>mb_[a-zA-Z0-9_]+</name>[\s\S]*?</include>"
content = re.sub(pattern, "", content)

# There are also posts from the original world like post_0, post_1, post_2
pattern_posts = r"<include>\s*(?:<pose>[^<]*</pose>\s*)?<name>post_[0-9]+</name>[\s\S]*?</include>"
content = re.sub(pattern_posts, "", content)

with open(os.path.join(get_workspace_root(), 'vrx/vrx_gz/worlds/bathymetry.sdf'), 'w') as f:
    f.write(content)

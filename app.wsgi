import sys
sys.path.insert(0, '/var/www/TweetMonitorAPI')

venv = ''
with open(venv) as file:
    exec(file.read(), dict(__file__=venv))

from api import app as application
"""
WSGI config for slackdice
"""
import os
import sys
import site

site.addsitedir('/home/apps/env/slackdice/lib/python3.4/site-packages')
sys.path.append('/home/apps/sites/slackdice')
sys.stdout = sys.stderr

from app import app as application

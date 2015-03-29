#!flask/bin/python
import os
import sys
if sys.platform == 'win32':
    pybabel = 'pybabel.exe'
else:
    pybabel = 'pybabel'
os.system(pybabel + ' compile -d app/translations')

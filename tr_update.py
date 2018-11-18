#!python27
import os
import sys
if sys.platform == 'wiin32':
    pybabel = 'pybabel.exe'
else:
    pybabel = 'pybabel'
os.system(pybabel + ' extract -F babel.cfg -k lazy_gettext -o messages.pot app')
os.system(pybabel + ' update -i messages.pot -d app/translations')
os.unlink('messages.pot')

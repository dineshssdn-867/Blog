#!c:\users\dinesh\desktop\fantom\myenv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'django-htmlmin==0.11.0','console_scripts','pyminify'
__requires__ = 'django-htmlmin==0.11.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('django-htmlmin==0.11.0', 'console_scripts', 'pyminify')()
    )

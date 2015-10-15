import sys, os

# Set LANG/Encoding
os.environ.update(dict(
    LANG='en_US.UTF-8',
    LC_ALL='en_US.UTF-8'
))

# Detect APP_ROOT
_curdir = os.path.abspath(os.curdir)
os.chdir(os.path.dirname(__file__))
SETTINGS_ROOT = os.path.abspath(os.curdir)
APP_ROOT = os.path.abspath('.')
os.chdir(_curdir); del _curdir

# Add APP_ROT to path
for root in [APP_ROOT]:
    if(root not in sys.path):
        sys.path.insert(0, root)

# Activate Virtualenv with Django and other requirements
for script_dir in ('bin', 'Scripts'):
    try:
        _pyenv = os.path.join(APP_ROOT, 'pyenv', script_dir, 'activate_this.py')
        execfile(_pyenv, dict(__file__=_pyenv))
        del _pyenv
    except:
        pass

# Clean up
del sys, os
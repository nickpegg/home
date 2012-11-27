ENV = 'development'

try:
    exec('from home.envs.%s import *' % ENV)
except ImportError:
    print("Could not load settings for the %s environment!" % ENV)

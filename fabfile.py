from fabric.api import *
from fabric.contrib.files import *

env.hosts = ['bertha']
env.base_dir = '/srv/virtual/home.nickpegg.com'

def deploy():
    local('git push deploy')
    
    with cd(env.base_dir + '/site'):
        run('git pull')
        
        with prefix('source ../bin/activate'):
            run('./manage.py migrate')
        
    sudo('supervisorctl restart home')

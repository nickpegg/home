from fabric.api import *

env.hosts = ['bertha']

def deploy():
    local('git push deploy deploy')
    
    with cd('/srv/home/site'):
        run('git pull origin deploy')
        
        with prefix('source ../bin/activate'):
            run('./manage.py migrate')
        
    sudo('supervisorctl restart home')

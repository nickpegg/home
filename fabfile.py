from fabric.api import *

env.hosts = ['bertha']

def deploy():
    with cd('/srv/home/site'):
        run('git pull')
        
        with prefix('source ../bin/activate'):
            run('./manage.py migrate')
        
    sudo('supervisorctl restart home')

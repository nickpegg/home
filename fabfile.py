from fabric.api import *

env.hosts = ['bertha']

def deploy():
    with cd('/srv/home/site'):
        sudo('git pull')
        
    sudo('supervisorctl restart home')

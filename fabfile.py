from fabric.api import *
from fabric.contrib.files import *

env.hosts = ['www.home.nickpegg.com']
env.base_dir = '/srv/virtual/home.nickpegg.com'


def deploy():
    local('git push deploy master')

    with cd(env.base_dir + '/site'):
        run('git pull')

        with prefix('source ../bin/activate'):
            run('pip install -r requirements.txt')
            run('./manage.py syncdb')
            run('./manage.py migrate')

    sudo('supervisorctl restart home')
    sudo('supervisorctl restart home_worker')

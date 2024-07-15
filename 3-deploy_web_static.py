#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""


from datetime import datetime
from fabric.api import put, run, env, local
import os


env.hosts = ['34.229.161.126', '54.146.59.87']
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_pack():
    """ Fabric script that generates a .tgz archive from the contents of the...
    ...web_static folder """
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)
    result = local("sudo tar -cvzf {} web_static".format(filename))
    filesize = os.path.getsize(filename)
    if result.succeeded:
        print(f"web_static packed: {filename} -> {filesize}Bytes")
        return filename
    else:
        return None


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        print("Changes Deployed")
        return True
    except:
        return False

def deploy():
    new_archive = do_pack()
    if not os.path.exists(new_archive):
        return False
    result = do_deploy(new_archive)
    return result

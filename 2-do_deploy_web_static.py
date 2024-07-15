#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
import os


env.hosts = ['34.229.161.126', '54.146.59.87']
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


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
        result = run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        if result.failed:
            print(f"Failed to extract: {result.stderr}")
            return False
        run('rm /tmp/{}'.format(file_n))
        result = run('rsync -a {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        if result.failed:
            print(f"Rsync failed: {result.stderr}")
            return False
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        print("Changes Deployed")
        return True
    except Exception as e:
        print(f"Failed to deploy: {e}")
        return False


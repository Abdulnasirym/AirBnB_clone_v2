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
    """Distributes an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run(f'mkdir -p {path}{no_ext}/')
        run(f'tar -xzf /tmp/{file_n} -C {path}{no_ext}/')
        run(f'rm /tmp/{file_n}')

        # Remove existing subdirectories if they exist
        run(f'rm -rf {path}{no_ext}/web_static')

        # Move files from the web_static directory to the release folder
        run(f'mv {path}{no_ext}/web_static/* {path}{no_ext}/')

        run(f'rm -rf {path}{no_ext}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {path}{no_ext}/ /data/web_static/current')
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False



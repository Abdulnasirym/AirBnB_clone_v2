#!/usr/bin/python3
"""
This module contains the function do_pack that generates a .tgz archive
from the contents of the web_static folder (fabric script)
"""


from datetime import datetime
from fabric.api import *
import os


env.hosts = ['34.229.161.126','54.146.59.87']
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_pack():
    """Fabric script that generates a .tgz archive from the contents of the...
    ...web_static folder
    """
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"versions/web_static_{date}.tgz"
    result = local(f"sudo tar -cvzf {filename} web_static")
    filesize = os.path.getsize(filename)
    if result.succeeded:
        print(f"web_static packed: {filename} -> {filesize}Bytes")
        return filename

def do_deploy(archive_path):
    # checks if if path exist
    if not os.path.exists(archive_path):
        return False
    try:
        # upload archive to /tmp/
        put(archive_path, "/tmp/")

        # creating the proper directory to extract to
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        run(f"mkdir -p /data/web_static/releases/{folder_name}/")

        # uncompressing to the directory
        run(f"tar -xzf /tmp/{file_name} -C /data/web_static/releases/{folder_name}/")

        # deleting the archive from the server
        run(f"rm /tmp/{file_name}")

        # moving the extracted files from the archive to the folder
        run(f"mv /data/web_static/releases/{folder_name}/web_static/* \
        /data/web_static/releases/{folder_name}/")
        run(f"rm -rf /data/web_static/releases/{folder_name}/web_static/")

        # Remove the current symbolic link and create a new one
        run("rm -rf /data/web_static/current")
        run(f"ln -s /data/web_static/releases/{folder_name}/ /data/web_static/current")
        print("New version deployed")
        return True
    except Exception as e:
        print(f"Deployed failed: {e}")
        return False

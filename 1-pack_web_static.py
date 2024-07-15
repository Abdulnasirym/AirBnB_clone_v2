#!/usr/bin/env python3
"""
Fabric script that generates a .tgz archive
from the contents of the web_static folder
of your AirBnB Clone repo
"""


from fabric.api import *
from datetime import datetime
import os


def do_pack():
    """
    Fabric script that
    generate a .tgz archive
    """
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"versions/web_static_{date}.tgz"
    result = local(f"sudo tar -cvzf {filename} web_static")
    filesize = os.path.getsize(filename)

    if result.succeeded:
        print(f"web_static packed: {filename} -> {filesize}Bytes")
    else:
        return None

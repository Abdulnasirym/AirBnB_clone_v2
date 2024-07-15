#!/usr/bin/python3
"""
Fabric script to clean up old static files from the web servers
"""

from fabric.api import run, env

env.hosts = ['34.229.161.126', '54.146.59.87']
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"

def clean_static_files():
    """Remove the static files and directories from the web servers"""
    try:
        # Remove the current symbolic link
        run("rm -rf /data/web_static/current")
        
        # Remove all directories inside releases
        run("rm -rf /data/web_static/releases/*")

        print("Static files cleaned up!")
        return True
    except Exception as e:
        print(f"Cleanup failed: {e}")
        return False


#!/usr/bin/python3
import os
from datetime import datetime
from fabric.api import local

def do_pack():
    """Generate a .tgz archive from web_static folder."""
    if not os.path.exits('versions'):
        os.makedirs('versions')
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"versions/web_static_{filename}.tgz"
    result = local("tar -cvzf {filename} web_static")
    if os.path.exists(filename) and result.succeeded:
        return filename
    return None

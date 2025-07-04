#!/usr/bin/python3
from datetime import datetime
import os
from invoke import task
@task
def do_pack(c):
    """Generate a .tgz archive from web_static."""
    os.makedirs("versions", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{timestamp}.tgz"
    print(f"Packing web_static to {archive_path}")
    cmd = f"tar -cvzf {archive_path} web_static"
    print(f"[localhost] local: {cmd}")
    result = c.run(cmd, warn=True)
    if result.ok:
        file_size = os.path.getsize(archive_path)
        print(f"web_static packed: {archive_path} -> {file_size}Bytes")
        print("Done.")
        return archive_path
    else:
        print("Packing failed.")
        return None

#!/usr/bin/env python3
"""
Fabric/Invoke 3 script that deletes out-of-date archives, for ALX AirBnB project.
Usage:
    invoke --collection=clean_web_static do-clean --number=<n>
"""
import os
from invoke import task, Collection
from fabric import Connection

@task
def do_clean(c, number=0):
    """
    Deletes out-of-date archives locally and on the web server.
    number: number of archives to keep (default is 0 => keep only the most recent one)
    """
    try:
        number = int(number)
    except ValueError:
        number = 0

    keep = 1 if number < 2 else number

    # Clean local versions folder
    local_archives = sorted(
        [f for f in os.listdir("versions") if f.endswith(".tgz")],
        key=lambda x: os.path.getmtime(os.path.join("versions", x)),
        reverse=True
    )

    for archive in local_archives[keep:]:
        archive_path = os.path.join("versions", archive)
        print(f"Removing local archive: {archive_path}")
        os.remove(archive_path)

    # Clean on remote server (localhost in this case)
    conn = Connection(
        host="127.0.0.1",
        user=os.getenv("USER"),
        connect_kwargs={"key_filename": os.path.expanduser("~/.ssh/id_rsa")}
    )

    result = conn.run("ls -1t /data/web_static/releases", hide=True, warn=True)
    remote_dirs = [d for d in result.stdout.strip().split('\n') if d.startswith("web_static_")]

    for dir_name in remote_dirs[keep:]:
        path = f"/data/web_static/releases/{dir_name}"
        print(f"Removing remote archive: {path}")
        conn.run(f"rm -rf {path}", warn=True)

# register task
ns = Collection()
ns.add_task(do_clean, name="do-clean")
namespace = ns


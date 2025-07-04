#!/usr/bin/python3
from fabric import task, Connection
from invoke import Collection
import os


@task
def do_deploy(c, archive_path):
    """Distribute an archive to the local server (127.0.0.1)."""
    if not os.path.exists(archive_path):
        print(f"Archive not found: {archive_path}")
        return False

    archive_name = os.path.basename(archive_path)
    name_no_ext = archive_name.replace(".tgz", "")
    release_path = f"/data/web_static/releases/{name_no_ext}/"
    tmp_path = f"/tmp/{archive_name}"

    # Manually create a new SSH connection to localhost
    conn = Connection(
        host="127.0.0.1",
        user="jamez",
        connect_kwargs={
            "key_filename": "/home/jamez/.ssh/id_rsa"
        }
    )

    try:
        print(f"[{conn.host}] put: {archive_path} -> {tmp_path}")
        conn.put(archive_path, tmp_path)

        print(f"[{conn.host}] run: mkdir -p {release_path}")
        conn.run(f"mkdir -p {release_path}")

        print(f"[{conn.host}] run: tar -xzf {tmp_path} -C {release_path}")
        conn.run(f"tar -xzf {tmp_path} -C {release_path}")

        print(f"[{conn.host}] run: rm {tmp_path}")
        conn.run(f"rm {tmp_path}")

        print(f"[{conn.host}] run: mv {release_path}web_static/* {release_path}")
        conn.run(f"mv {release_path}web_static/* {release_path}")

        print(f"[{conn.host}] run: rm -rf {release_path}web_static")
        conn.run(f"rm -rf {release_path}web_static")

        print(f"[{conn.host}] run: rm -rf /data/web_static/current")
        conn.run("rm -rf /data/web_static/current")

        print(f"[{conn.host}] run: ln -s {release_path} /data/web_static/current")
        conn.run(f"ln -s {release_path} /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

ns = Collection()
ns.add_task(do_deploy, name="do-deploy")
namespace = ns

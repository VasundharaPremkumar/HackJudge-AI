
import docker
from docker_manager import create_container, start_container


def execute_project(client, project_dir, filename="main.py"):
    container = None

    try:
        container = create_container(client, project_dir)

        start_container(container)

        result = container.exec_run(
        ["timeout", "10s", "python", filename],
        workdir="/workspace",
         demux=True
)

        stdout, stderr = result.output

        return {
            "exit_code": result.exit_code,
            "stdout": stdout.decode() if stdout else "",
            "stderr": stderr.decode() if stderr else ""
        }

    except docker.errors.DockerException as e:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e)
        }

    finally:
        if container:
            container.remove(force=True)

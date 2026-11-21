import docker
from pathlib import Path

IMAGE_NAME="hackjudge-python:1.0"

def get_docker_client():
    try:
        client=docker.DockerClient(base_url="npipe:////./pipe/dockerDesktopLinuxEngine")
        client.ping()
        print("Docker connection successful!")
        return client
    except docker.errors.DockerException as e:
        print(f"Docker connection failed: {e}")
        return None

def create_container(client,project_dir):
     project_path=Path(project_dir).resolve()
     if not project_path.is_dir():
          raise ValueError("Project directory does not exist")

if __name__=="__main__":
        client=get_docker_client()
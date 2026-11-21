import docker

def get_docker_client():
    try:
        client=docker.DockerClient(base_url="npipe:////./pipe/dockerDesktopLinuxEngine")
        client.ping()
        print("Docker connection successful!")
        return client
    except docker.errors.DockerException as e:
        print(f"Docker connection failed: {e}")
        return None
    
if __name__=="__main__":
        client=get_docker_client()
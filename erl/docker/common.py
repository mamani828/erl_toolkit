import docker


def get_container(name: str):
    client = docker.from_env()
    containers = client.containers.list(all=True, filters={"name": name})
    if containers is None or len(containers) == 0:
        return None
    elif len(containers) == 1:
        return containers[0]
    else:
        raise RuntimeError(f"More than 1 container have name: {name}?!")

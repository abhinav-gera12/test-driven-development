import docker
import docker.errors
import time
import os

def is_container_ready(container):
    container.reload()
    return container.status == "Running"

def wait_for_stable_status(container, stable_duration=3, interval=1):
    start_time = time.time()
    stable_count = 0
    while time.time() - start_time < stable_duration:
        if is_container_ready(container):
            stable_count += 1
        else:
            stable_count = 0
            
        if stable_count >= stable_duration / interval:
            return True
        time.sleep(interval)
    return False
    

def start_database_container():
    client = docker.from_env()
    scripts_dir = os.path.abspath("./scripts")
    container_name = "test_db"
    
    try:
        existing_container = client.containers.get(container_name)
        print(f"Container {container_name} exists. Stopping and Removing")
        existing_container.stop()
        existing_container.remove()
        print(f"Container {container_name} stopped and removed")
    except docker.errors.NotFound:
        print(f"Container {container_name} doesn't not exist")
        
    
    #define the container configuration
    container_config = {
        "name":container_name,
        "image": "postgres:16.3-bullseye",
        "detach": True,
        "ports": {"5432":"5434"},
        "environment": {
            "POSTGRES_USER":"postgres",
            "POSTGRES_PASSWORD": "postgres",
        },
        "volumes": [f"{scripts_dir}:/docker-entrypoint-initdb.d"],
    }
    
    container = client.containers.run(**container_config)
    
    while not is_container_ready(container):
        time.sleep(1)
        
    if not wait_for_stable_status(container):
        raise RuntimeError("Container did not stablize within the specified time")
    
    return container
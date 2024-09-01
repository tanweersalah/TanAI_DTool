import docker
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

app = FastAPI()
client = docker.from_env()

class ContainerInfo(BaseModel):
    id: str
    name: str
    status: str
    image: str
    created: str
    ports: Dict[str, Any]
    labels: Dict[str, str]
    network_settings: Dict[str, Any]
    mounts: List[Dict[str, Any]]
    state: Dict[str, Any]
    host_config: Dict[str, Any]

class LogEntry(BaseModel):
    timestamp: str
    message: str

class ContainerLogs(BaseModel):
    container_id: str
    logs: List[LogEntry]

@app.get("/containers", response_model=List[ContainerInfo])
async def list_containers():
    containers = client.containers.list(all=True)
    container_info_list = []
    for container in containers:
        # Refresh container attributes
        container.reload()
        
        container_info = ContainerInfo(
            id=container.id,
            name=container.name,
            status=container.status,
            image=container.image.tags[0] if container.image.tags else container.image.id,
            created=container.attrs['Created'],
            ports={k: v for k, v in container.attrs['NetworkSettings']['Ports'].items() if v is not None},
            labels=container.labels,
            network_settings=container.attrs['NetworkSettings'],
            mounts=container.attrs['Mounts'],
            state=container.attrs['State'],
            host_config={
                'RestartPolicy': container.attrs['HostConfig']['RestartPolicy'],
                'AutoRemove': container.attrs['HostConfig']['AutoRemove'],
                'Runtime': container.attrs['HostConfig']['Runtime'],
                'Privileged': container.attrs['HostConfig']['Privileged'],
            }
        )
        container_info_list.append(container_info)
    return container_info_list

@app.get("/logs/{container_id}", response_model=ContainerLogs)
async def get_container_logs(
    container_id: str, 
    filter_errors: Optional[bool] = Query(False, description="Filter for error logs"),
    tail: Optional[int] = Query(100, description="Number of log lines to retrieve")
):
    try:
        container = client.containers.get(container_id)
        logs = container.logs(tail=tail, stderr=True, stdout=True, timestamps=True).decode('utf-8')
        
        log_entries = []
        for line in logs.strip().split('\n'):
            parts = line.split(' ', 1)
            if len(parts) == 2:
                timestamp, message = parts
                if not filter_errors or 'error' in message.lower():
                    log_entries.append(LogEntry(timestamp=timestamp, message=message))

        return ContainerLogs(container_id=container_id, logs=log_entries)
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Container not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
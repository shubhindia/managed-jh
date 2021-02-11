import docker
client = docker.DockerClient(base_url='tcp://127.0.0.1:2375')
print(client.containers.list())

#this will come from request body
container_name = 'shubhi-managed-jh-instance'
volumes = {'/Users/shubhcyanogen/Desktop/managed-jh/test':{'bind': '/home/jovyan/work', 'mode': 'rw'}}
print(volumes)
container = client.containers.run('jupyter/scipy-notebook',detach=True, publish_all_ports=True,
                                    volumes=volumes, name=container_name)

i = 0
for n,line in enumerate(container.logs(stream=True)):
    print(n)
    if n == 20:
        
        token_url = line.strip()
        break
    

jh_token = str(token_url).split("=")[-1].replace("'","")

container = client.containers.get(container_id=container_name)

port = container.__dict__['attrs']['NetworkSettings']['Ports']['8888/tcp'][0]['HostPort']

url = 'localhost:' + port + '/?token=' + jh_token

print(url)

# So far this script can launch a notebook instance 
# TO DO : make volumes dynamic, get container id and list exposed port as well
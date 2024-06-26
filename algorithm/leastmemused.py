import os
import time
import requests
import subprocess

PROMETHEUS_URL = "http://prometheus-the-collector-svc.duchm-monitoring.svc.cluster.local:9090"

last_server = None  # Variable to store the last known server with lowest ram Usage Idle

def query_prometheus(query):
    url = f"{PROMETHEUS_URL}/api/v1/query"
    params = {"query": query}
    print(f"Querying Prometheus at {url} with params: {params}")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        raise Exception(f"Query failed: {e}")

def find_server_with_lowest_ram_idle(instances):
    min_ram_idle = float('inf')  # Start with a very large number
    instance_with_min_mem_idle = None
    
    for instance in instances:
        ram_idle = float(instance['value'][1])  # Convert ram Usage Idle to float
        if ram_idle < min_ram_idle:
            min_ram_idle = ram_idle
            instance_with_min_mem_idle = instance
    
    if instance_with_min_mem_idle:
        return instance_with_min_mem_idle['metric']['instance'], min_ram_idle
    else:
        raise Exception("No valid instance found with ram Usage Idle.")

def generate_nginx_config(server):
    global last_server  # Declare last_server as global here
    
    nginx_config = f'''
    server {{
        listen 80;
        server_name your_domain.com;

        location / {{
            proxy_pass http://{server};
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}
    }}
    '''
    
    nginx_config_file = 'nginx.conf'
    
    # Check if server has changed or nginx config file does not exist
    if server != last_server or not os.path.exists(nginx_config_file):
        try:
            with open(nginx_config_file, 'w') as f:
                f.write(nginx_config)
            
            print("Nginx configuration file generated successfully.")
            
            # Restart nginx
            restart_nginx()
            
            # Update last_server
            last_server = server
        except IOError as e:
            print(f"Error writing nginx config file: {e}")
    else:
        print("Nginx configuration file already up-to-date.")

def restart_nginx():
    print("Restarting nginx...")
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'], check=True)
        print("Nginx restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Nginx restart failed: {e}")

def main():
    try:
        while True:
            # Example query to get Ram Usage Idle for all servers
            query = 'mem_available'
            
            # Query Prometheus
            result = query_prometheus(query)
            
            instances = result['data']['result']
            
            # Find server with lowest ram Usage Idle
            server, mem_used = find_server_with_lowest_ram_idle(instances)
            
            # Generate nginx configuration file if server has changed
            generate_nginx_config(server)
            
            print(f"Request will be proxied to server {server} with lowest Ram Usage Idle: {mem_used}")
            
            # Sleep for 5 seconds before querying Prometheus again
            time.sleep(5)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

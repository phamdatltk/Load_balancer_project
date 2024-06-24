import time
import os
import requests

# Function to query Prometheus
def query_prometheus(query, url):
    params = {'query': query}
    response = requests.get(f'{url}/api/v1/query', params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            return data
    return None

# Function to get the server with least response time
def least_response_time(servers, prometheus_url):
    response_times = []
    for server in servers:
        response_query = 'rate(http_request_duration_seconds_sum[1m]) / rate(http_request_duration_seconds_count[1m])'
        response_data = query_prometheus(response_query, prometheus_url)
        if response_data and 'data' in response_data and 'result' in response_data['data'] and len(response_data['data']['result']) > 0:
            response_time = float(response_data['data']['result'][0]['value'][1])
            response_times.append((server, response_time))
        else:
            print(f"No valid response time data received from Prometheus for server {server}")
    if response_times:
        return min(response_times, key=lambda x: x[1])[0]
    else:
        return None

def generate_nginx_conf(server):
    conf = f"""
http {{
    upstream backend {{
        least_conn;
        server {server};
    }}

    server {{
        location / {{
            proxy_pass http://backend;
            health_check;
        }}
        location /api {{
            limit_except GET {{
                auth_basic "NGINX Plus API";
                auth_basic_user_file /path/to/passwd/file;
            }}
            api write=on;
            allow 127.0.0.1;
            deny  all;
        }}
    }}
}}
"""
    return conf

def main():
    servers = [
        'http://mem-simpleapp-0.kllr-mem-svc.duchm.svc.cluster.local:8080',
        'http://mem-simpleapp-1.kllr-mem-svc.duchm.svc.cluster.local:8080',
        'http://mem-simpleapp-2.kllr-mem-svc.duchm.svc.cluster.local:8080',
        'http://cpu-simpleapp-0.kllr-cpu-svc.duchm.svc.cluster.local:8080',
        'http://cpu-simpleapp-1.kllr-cpu-svc.duchm.svc.cluster.local:8080',
        'http://cpu-simpleapp-2.kllr-cpu-svc.duchm.svc.cluster.local:8080'
    ]
    prometheus_url = 'http://prometheus-the-collector-svc.duchm-monitoring.svc.cluster.local:9090'

    while True:
        # Get the server with the least response time
        best_server = least_response_time(servers, prometheus_url)
        if best_server:
            print(f"Server with least response time: {best_server}")

            # Generate and save the Nginx configuration file
            nginx_conf = generate_nginx_conf(best_server)
            with open('nginx.conf', 'w', encoding='utf-8') as f:
                f.write(nginx_conf)
            print("Nginx configuration file (nginx.conf) generated successfully!")

            time.sleep(1)  # Wait for 1 second
            # Delete the old configuration file
            if os.path.exists('nginx.conf'):
                os.remove('nginx.conf')
                print("Old Nginx configuration file (nginx.conf) deleted!")
        else:
            print("No valid response time data received from Prometheus servers.")

        time.sleep(20)  # Wait for 20 seconds

if __name__ == "__main__":
    main()

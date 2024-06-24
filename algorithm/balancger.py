import time
import os
import requests

# Function to query Prometheus
def query_prometheus(query, url):
    params = {'query': query}
    response = requests.get(f'{url}/api/v1/query', params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success' and data['data']['result']:
            return float(data['data']['result'][0]['value'][1])
    return None

def get_metric(server, query):
    prometheus_url = f"http://{server}:9090"
    return query_prometheus(query, prometheus_url)

def generate_nginx_conf(servers, weights):
    conf = """
http {
    upstream backend {
        least_conn;
""" 
    for server, weight in zip(servers, weights):
        conf += f"        server {server} weight={weight};\n"
        
    conf += """
    }

    server {
        location / {
            proxy_pass http://backend;
            health_check;
        }
        location /api {
            limit_except GET {
                auth_basic "NGINX Plus API";
                auth_basic_user_file /path/to/passwd/file;
            }
            api write=on;
            allow 127.0.0.1;
            deny  all;
        }
    }
}
"""
    return conf

def main():
    servers = ['server1.example.com', 'server2.example.com', 'server3.example.com']

    while True:
        metrics = {
            'response_time': 'rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])',
            'cpu': '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)',
            'memory': '100 * (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes',
            'disk': '100 * (1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}))',
            'bandwidth': 'rate(node_network_receive_bytes_total[5m]) + rate(node_network_transmit_bytes_total[5m])'
        }
        
        metric_values = {metric: [] for metric in metrics}
        
        for server in servers:
            for metric, query in metrics.items():
                value = get_metric(server, query)
                if value is not None:
                    metric_values[metric].append((server, value))

        server_weights = {server: 0 for server in servers}

        for metric in metrics:
            sorted_servers = sorted(metric_values[metric], key=lambda x: x[1])
            for rank, (server, _) in enumerate(sorted_servers):
                server_weights[server] += (len(servers) - rank)

        weights = [server_weights[server] for server in servers]

        nginx_conf = generate_nginx_conf(servers, weights)
        with open('nginx.conf', 'w', encoding='utf-8') as f:
            f.write(nginx_conf)
        print("Nginx configuration file (nginx.conf) generated successfully!")

        time.sleep(20)  # Chờ 20 giây
        # Xóa tệp cũ
        if os.path.exists('nginx.conf'):
            os.remove('nginx.conf')
            print("Old Nginx configuration file (nginx.conf) deleted!")

if __name__ == "__main__":
    main()

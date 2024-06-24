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
def least_response_time(servers):
    response_times = []
    for server in servers:
        prometheus_url = f"http://{server}:9090"
        response_query = 'rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])'
        response_data = query_prometheus(response_query, prometheus_url)
        if response_data:
            response_time = float(response_data['data']['result'][0]['value'][1])
            response_times.append((server, response_time))
    return min(response_times, key=lambda x: x[1])[0]

# Function to get the server with least utilized memory
def least_utilized_memory(servers):
    mem_utilizations = []
    for server in servers:
        prometheus_url = f"http://{server}:9090"
        mem_query = '100 * (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes'
        mem_data = query_prometheus(mem_query, prometheus_url)
        if mem_data:
            mem_utilization = float(mem_data['data']['result'][0]['value'][1])
            mem_utilizations.append((server, mem_utilization))
    return min(mem_utilizations, key=lambda x: x[1])[0]

# Function to get the server with least utilized disk
def least_utilized_disk(servers):
    disk_utilizations = []
    for server in servers:
        prometheus_url = f"http://{server}:9090"
        disk_query = '100 * (1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}))'
        disk_data = query_prometheus(disk_query, prometheus_url)
        if disk_data:
            disk_utilization = float(disk_data['data']['result'][0]['value'][1])
            disk_utilizations.append((server, disk_utilization))
    return min(disk_utilizations, key=lambda x: x[1])[0]

# Function to get the server with least utilized CPU
def least_utilized_cpu(servers):
    cpu_utilizations = []
    for server in servers:
        prometheus_url = f"http://{server}:9090"
        cpu_query = '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
        cpu_data = query_prometheus(cpu_query, prometheus_url)
        if cpu_data:
            cpu_utilization = float(cpu_data['data']['result'][0]['value'][1])
            cpu_utilizations.append((server, cpu_utilization))
    return min(cpu_utilizations, key=lambda x: x[1])[0]

# Function to get the server with least width of bandwidth
def least_bandwidth(servers):
    bandwidths = []
    for server in servers:
        prometheus_url = f"http://{server}:9090"
        network_query = 'rate(node_network_receive_bytes_total[5m]) + rate(node_network_transmit_bytes_total[5m])'
        network_data = query_prometheus(network_query, prometheus_url)
        if network_data:
            bandwidth = float(network_data['data']['result'][0]['value'][1])
            bandwidths.append((server, bandwidth))
    return min(bandwidths, key=lambda x: x[1])[0]

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
    #best bandwidth
    while True:
        # Lấy máy chủ có băng thông sử dụng ít nhất
        best_server_bandwidth = least_bandwidth(servers)
        if best_server_bandwidth:
            print(f"Server with least bandwidth usage: {best_server_bandwidth}")

            # Tạo và lưu file cấu hình Nginx chỉ với máy chủ có băng thông sử dụng ít nhất
            nginx_conf = generate_nginx_conf(best_server_bandwidth)
            with open('nginx.conf', 'w', encoding='utf-8') as f:
                f.write(nginx_conf)
            print("Nginx configuration file (nginx.conf) generated successfully!")

            time.sleep(1)  # Chờ 20 giây
            # Xóa tệp cũ
            if os.path.exists('nginx.conf'):
                os.remove('nginx.conf')
                print("Old Nginx configuration file (nginx.conf) deleted!")
        else:
            print("No valid bandwidth data received from Prometheus servers.")

    # while True:
    #     # Get the server with the least response time
    #     best_server_response_time = least_response_time(servers)
    #     print(f"Server with least response time: {best_server_response_time}")

    #     # Get the server with the least utilized memory
    #     best_server_memory = least_utilized_memory(servers)
    #     print(f"Server with least utilized memory: {best_server_memory}")

    #     # Get the server with the least utilized disk
    #     best_server_disk = least_utilized_disk(servers)
    #     print(f"Server with least utilized disk: {best_server_disk}")

    #     # Get the server with the least utilized CPU
    #     best_server_cpu = least_utilized_cpu(servers)
    #     print(f"Server with least utilized CPU: {best_server_cpu}")

    #     # Get the server with the least width of bandwidth
    #     best_server_bandwidth = least_bandwidth(servers)
    #     print(f"Server with least bandwidth usage: {best_server_bandwidth}")

    #     # For the purpose of NGINX configuration, calculate weights based on a specific logic
    #     # You can define a logic that combines the results from the above functions
    #     # For simplicity, let's use an arbitrary weighting scheme here
    #     weights = [1, 2, 3]  # Placeholder for weights

        # Generate and save NGINX configuration file
        nginx_conf = generate_nginx_conf(servers, weights)
        with open('nginx.conf', 'w', encoding='utf-8') as f:
            f.write(nginx_conf)
        print("Nginx configuration file (nginx.conf) generated successfully!")

        time.sleep(20)  # Wait for 20 seconds
        # Delete the old configuration file
        if os.path.exists('nginx.conf'):
            os.remove('nginx.conf')
            print("Old Nginx configuration file (nginx.conf) deleted!")

if __name__ == "__main__":
    main()

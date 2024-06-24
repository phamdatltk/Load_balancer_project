import time
import os
import requests

# Function to query Prometheus
def query_prometheus(query, url="http://your-prometheus-url.com:9090"):
    params = {'query': query}
    response = requests.get(f'{url}/api/v1/query', params=params)
    data = response.json()
    return data




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
            proxy_pass http://appservers;
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

def calculate_weight(mem_percent, cpu_percent, disk_percent, network_percent, request_ratio, k1, k2, k3, k4, k5):
    return mem_percent * k1 + cpu_percent * k2 + disk_percent * k3 + network_percent * k4 + request_ratio * k5


def main():
    servers = ['server1.example.com', 'server2.example.com', 'server3.example.com']
    k1 = float(input("Enter coefficient k1: "))
    k2 = float(input("Enter coefficient k2: "))
    k3 = float(input("Enter coefficient k3: "))
    k4 = float(input("Enter coefficient k4: "))
    k5 = float(input("Enter coefficient k5: "))

    while True:
        mem_percent_list = []
        cpu_percent_list = []
        disk_percent_list = []
        network_percent_list = []
        request_ratio_list = []

        for server in servers:
            # Lấy thông số từ Prometheus
            mem_query = f'100 * (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes'
            cpu_query = '100 - (rate(node_cpu_seconds_total{mode="idle"}[5m]) * 100)'
            disk_query = '100 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100'
            network_query = 'rate(node_network_receive_bytes_total[5m]) + rate(node_network_transmit_bytes_total[5m])'

            mem_data = query_prometheus(mem_query, f"http://{server}:9090")
            cpu_data = query_prometheus(cpu_query, f"http://{server}:9090")
            disk_data = query_prometheus(disk_query, f"http://{server}:9090")
            network_data = query_prometheus(network_query, f"http://{server}:9090")
            request_ratio_data = query_prometheus('your_request_ratio_query_here', f"http://{server}:9090")

            # Xử lý dữ liệu từ Prometheus để lấy giá trị cần thiết
            mem_percent = mem_data['data']['result'][0]['value'][1]
            cpu_percent = cpu_data['data']['result'][0]['value'][1]
            disk_percent = disk_data['data']['result'][0]['value'][1]
            network_percent = network_data['data']['result'][0]['value'][1]
            request_ratio = request_ratio_data['data']['result'][0]['value'][1]

            mem_percent_list.append(mem_percent)
            cpu_percent_list.append(cpu_percent)
            disk_percent_list.append(disk_percent)
            network_percent_list.append(network_percent)
            request_ratio_list.append(request_ratio)

        weights = []
        for mem_percent, cpu_percent, disk_percent, network_percent, request_ratio in zip(mem_percent_list, cpu_percent_list, disk_percent_list, network_percent_list, request_ratio_list):
            weight = calculate_weight(mem_percent, cpu_percent, disk_percent, network_percent, request_ratio, k1, k2, k3, k4, k5)
            weights.append(weight)

        # Tạo và lưu file cấu hình Nginx
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

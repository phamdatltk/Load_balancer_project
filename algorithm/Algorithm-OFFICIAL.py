import requests
import argparse
import subprocess
import time

def get_weights(prometheus_server, pod_name):
    prometheus_url = f'http://{prometheus_server}/api/v1/query'
    query = f'sum(kube_pod_container_resource_limits{{pod="{pod_name}", resource="cpu"}}) - sum(rate(container_cpu_usage_seconds_total{{pod="{pod_name}"}}[1m]))'
    print(query)
    response = requests.get(prometheus_url, params={'query': query})
    if response.status_code == 200:
        results = response.json()['data']['result']
        if results:
            value = results[0]['value'][1]
            weight = int(float(value) * 100 )
            if weight <= 0:
                weight = 1
            return weight
        else:
            print("Không có kết quả nào từ Prometheus.")
            return None
    else:
        print(f"Lỗi khi truy vấn Prometheus: {response.status_code}")
        return None

def create_config_file(prometheus_server, path):
    weight0 = get_weights(prometheus_server, "simpleapp-set1-0")
    print("Weight 0: " + str(weight0))
    weight1 = get_weights(prometheus_server, "simpleapp-set2-0")
    print("Weight 1: " + str(weight0))
    weight2 = get_weights(prometheus_server, "simpleapp-set3-0")
    print("Weight 2: " + str(weight0))

    config_content = f"""
upstream backend {{
   server simpleapp-set1-service weight={weight0};
   server simpleapp-set2-service weight={weight1};
   server simpleapp-set3-service weight={weight2};
}}
server {{
    listen 8081;
    server_name localhost;
    location / {{
        proxy_pass http://backend/;
    }}
}}
    """

    # Ghi nội dung vào file
    if weight0 != None and weight1 != None and weight2 != None:
      with open(path, 'w') as file:
         file.write(config_content.strip())
      return True
    return False

def apply_config_file(check):
   if check == True:
      try:
         # Gọi lệnh nginx -s reload để reload cấu hình Nginx
         result = subprocess.run(['nginx', '-s', 'reload'], check=True, capture_output=True, text=True)
         print(f"Config file đã được áp dụng và Nginx đã reload thành công.")
         print(result.stdout)  # In thông tin từ lệnh nginx -s reload (nếu cần)
      except subprocess.CalledProcessError as e:
         print(f"Lỗi khi reload Nginx: {e.stderr}")
      except FileNotFoundError:
         print("Lệnh nginx không tìm thấy. Hãy chắc chắn rằng Nginx đã được cài đặt và có sẵn trong PATH.")


def main():
    parser = argparse.ArgumentParser(description='Truy vấn lượng CPU còn có thể sử dụng từ Prometheus.')
    parser.add_argument('prometheus_server', type=str, help='URL của Prometheus server (ví dụ: localhost:9092)')
    args = parser.parse_args()
    while(True):
      try:
         check = create_config_file(prometheus_server=args.prometheus_server, path="/etc/nginx/conf.d/datpt.conf")
         apply_config_file(check=check)
      except Exception as e:
         print(e)
         time.sleep(1)
         continue
      time.sleep(2)
if __name__ == '__main__':
    main()

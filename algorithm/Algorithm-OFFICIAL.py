import requests
import argparse
import subprocess
import time
import logging

# Cấu hình logging
logging.basicConfig(filename="custom_log.log", level=logging.INFO, 
                    format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Các bước thực hiện:
# - B1: Tìm trọng số của từng pod
# - B2: Đưa trọng số vào trong file config
# - B3: Reload file config để NGINX nhận config mới
# - B4: Lặp liên tục các hành động trên

# Hàm này để lấy ra trọng số của từng pod, có thêm logic retry
def get_weights(prometheus_server, pod_name, retries=50, delay=0.5):
    prometheus_url = f'http://{prometheus_server}/api/v1/query'
    query = f'sum(kube_pod_container_resource_limits{{pod="{pod_name}", resource="cpu"}}) - sum(rate(container_cpu_usage_seconds_total{{pod="{pod_name}"}}[1m]))'
    
    # Lặp retries nếu không trả ra số liệu
    for attempt in range(retries):
        log_message = f"Attempt {attempt + 1}: {query}"
        print(log_message)
        logging.info(log_message)
        
        response = requests.get(prometheus_url, params={'query': query})
        
        if response.status_code == 200:
            results = response.json()['data']['result']
            if results:
                value = results[0]['value'][1]
                weight = int(float(value) * 10)
                if weight <= 0:
                    weight = 1
                return weight
            else:
                log_message = "Không có kết quả nào từ Prometheus, thử lại..."
                print(log_message)
                logging.info(log_message)
        else:
            log_message = f"Lỗi khi truy vấn Prometheus: {response.status_code}, thử lại..."
            print(log_message)
            logging.info(log_message)
        
        # Đợi trước khi thử lại
        time.sleep(delay)
    
    # Nếu sau retries mà vẫn không thành công
    log_message = f"Không thể lấy dữ liệu cho pod {pod_name} sau {retries} lần thử."
    print(log_message)
    logging.info(log_message)
    return None

# Hàm này để tạo config file cho NGINX, hàm trả True nếu file config hợp lệ, trả ra false nếu file config không hợp lệ
def create_config_file(prometheus_server, path):
    
    weight0 = get_weights(prometheus_server, "simpleapp-set1-0")
    log_message = f"Weight 0: {weight0}"
    print(log_message)
    logging.info(log_message)
    
    weight1 = get_weights(prometheus_server, "simpleapp-set2-0")
    log_message = f"Weight 1: {weight1}"
    print(log_message)
    logging.info(log_message)
    
    weight2 = get_weights(prometheus_server, "simpleapp-set3-0")
    log_message = f"Weight 2: {weight2}"
    print(log_message)
    logging.info(log_message)

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

# Hàm này để reload config trong NGINX nếu file config hợp lệ (Được kiểm tra bằng biến check)
def apply_config_file(check):
   if check == True:
      try:
         # Gọi lệnh nginx -s reload để reload cấu hình Nginx
         result = subprocess.run(['nginx', '-s', 'reload'], check=True, capture_output=True, text=True)
         print(f"Config file đã được áp dụng và Nginx đã reload thành công.")
         logging.info("Config file đã được áp dụng và Nginx đã reload thành công.")
         print(result.stdout)  # In thông tin từ lệnh nginx -s reload (nếu cần)
      except subprocess.CalledProcessError as e:
         print(f"Lỗi khi reload Nginx: {e.stderr}")
         logging.info(f"Lỗi khi reload Nginx: {e.stderr}")
      except FileNotFoundError:
         print("Lệnh nginx không tìm thấy. Hãy chắc chắn rằng Nginx đã được cài đặt và có sẵn trong PATH.")
         logging.info("Lệnh nginx không tìm thấy. Hãy chắc chắn rằng Nginx đã được cài đặt và có sẵn trong PATH.")


def main():
    # Truyền biến URL khi chạy chương trình
    parser = argparse.ArgumentParser(description='Truy vấn lượng CPU còn có thể sử dụng từ Prometheus.')
    parser.add_argument('prometheus_server', type=str, help='URL của Prometheus server (ví dụ: localhost:9092)')
    args = parser.parse_args()
    # Tạo vòng lặp để thuật toán hoạt động
    while(True):
      try:
         # Tạo biến check để kiểm tra file config hợp lệ hay không
         check = create_config_file(prometheus_server=args.prometheus_server, path="/etc/nginx/conf.d/datpt.conf")
         apply_config_file(check=check)
      except Exception as e:
         print(e)
         logging.error("Error: " + str(e))
         time.sleep(1)
         continue
      time.sleep(2)
if __name__ == '__main__':
    main()

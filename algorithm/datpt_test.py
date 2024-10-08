import requests
import time
import logging

# Cấu hình logging
logging.basicConfig(filename="custom_log.log", level=logging.INFO, 
                    format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Hàm này để lấy ra trọng số của từng pod, có thêm logic retry
def get_weights(prometheus_server, pod_name, retries=50, delay=0.5):
    prometheus_url = f'http://{prometheus_server}/api/v1/query'
    query = f'sum(kube_pod_container_resource_limits{{pod="{pod_name}", resource="cpu"}}) - sum(rate(container_cpu_usage_seconds_total{{pod="{pod_name}"}}[1m]))'
    
    for attempt in range(retries):
        log_message = f"Attempt {attempt + 1}: {query}"
        print(log_message)
        logging.info(log_message)
        
        response = requests.get(prometheus_url, params={'query': query})
        
        if response.status_code == 200:
            results = response.json()['data']['result']
            if results:
                value = results[0]['value'][1]
                weight = int(float(value) * 100)
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

# Truy vấn Prometheus và in ra kết quả với thời gian hiện tại
for i in range(100):

    weight0 = get_weights('localhost:38579', "simpleapp-set1-0")
    log_message = f"Weight 0: {weight0}"
    print(log_message)
    logging.info(log_message)
    
    weight1 = get_weights('localhost:38579', "simpleapp-set2-0")
    log_message = f"Weight 1: {weight1}"
    print(log_message)
    logging.info(log_message)
    
    weight2 = get_weights('localhost:38579', "simpleapp-set3-0")
    log_message = f"Weight 2: {weight2}"
    print(log_message)
    logging.info(log_message)

    # Có thể thêm độ trễ nhỏ giữa các vòng lặp nếu cần
    time.sleep(1)

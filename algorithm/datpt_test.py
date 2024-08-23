import requests

PROMETHEUS_URL = "http://localhost:44599"

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

def get_cpu_usage(data):
    instances_cpu_usage = {}
    results = data.get('data', {}).get('result', [])
    for result in results:
        instance = result['metric']['instance']
        cpu_idle = float(result['value'][1])
        cpu_usage = 100.0 - cpu_idle
        
        if instance not in instances_cpu_usage:
            instances_cpu_usage[instance] = 0.0
        instances_cpu_usage[instance] += cpu_usage
    
    return instances_cpu_usage

# Truy vấn Prometheus và in ra kết quả
data = query_prometheus("cpu_usage_idle")
cpu_usages = get_cpu_usage(data)
for instance, usage in cpu_usages.items():
    print(f"Instance: {instance}, Total CPU Usage: {usage:.2f}%")
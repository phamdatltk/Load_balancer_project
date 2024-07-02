import requests

PROMETHEUS_URL = "http://prometheus-the-collector-svc.duchm-monitoring.svc.cluster.local:9090"

def query_prometheus(query):
    url = f"{PROMETHEUS_URL}/api/v1/query"
    params = {"query": query}
    print(f"Querying Prometheus at {url} with params: {params}")
    response = requests.get(url, params=params)
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response JSON: {response.json()}")
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

def main():
    try:
        # Example query for CPU utilization using cpu_usage_idle
        query = "cpu_usage_idle"
        
        # Query Prometheus
        result = query_prometheus(query)
        
        # Process the response as needed
        if 'result' in result['data']:
            for metric in result['data']['result']:
                instance = metric['metric'].get('instance', 'unknown')
                value = metric['value'][1]
                print(f"Instance: {instance}, CPU Usage Idle: {value}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

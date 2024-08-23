from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Cấu hình kết nối tới Kubernetes Cluster (sử dụng kubeconfig)
config.load_kube_config("./algorithm/ypx1w7r0-kubeconfig")

# Hoặc sử dụng cấu hình mặc định khi chạy từ bên trong cluster
# config.load_incluster_config()

# Tạo API client cho metrics.k8s.io
api = client.CustomObjectsApi()

namespace = "duchm"  # Thay thế bằng namespace của bạn
group = "metrics.k8s.io"
version = "v1beta1"
plural = "pods"

# try:
# Lấy thông tin về metrics của các pod
metrics = api.list_namespaced_custom_object(
   group=group, version=version, namespace=namespace, plural=plural
)
for item in metrics["items"]:
   pod_name = item["metadata"]["name"]
   usage = item["containers"][0]["usage"]
   cpu_usage = usage["cpu"]
   memory_usage = usage["memory"]

   print(f"Pod: {pod_name}")
   print(f"CPU Usage: {cpu_usage}")
   print(f"Memory Usage: {memory_usage}")
   print()

# except Exception as e:
#     print(f"Exception when calling CustomObjectsApi->list_namespaced_custom_object: {e}")

core_api = client.CoreV1Api()

# Lấy thông tin pod
pods = core_api.list_namespaced_pod(namespace=namespace)

for pod in pods.items:
    pod_name = pod.metadata.name
    for container in pod.spec.containers:
        requests = container.resources.requests
        limits = container.resources.limits

        if requests:
            cpu_request = requests.get("cpu", "Unknown")
            memory_request = requests.get("memory", "Unknown")
        else:
            cpu_request = "Unknown"
            memory_request = "Unknown"

        if limits:
            cpu_limit = limits.get("cpu", "Unknown")
            memory_limit = limits.get("memory", "Unknown")
        else:
            cpu_limit = "Unknown"
            memory_limit = "Unknown"

        print(f"Pod: {pod_name}")
        print(f"CPU Request: {cpu_request}")
        print(f"Memory Request: {memory_request}")
        print(f"CPU Limit: {cpu_limit}")
        print(f"Memory Limit: {memory_limit}")
        print()
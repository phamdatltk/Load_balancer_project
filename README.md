# Load balancer project

![alt text](image.png)

# Dựng pod backend đơn giản
## Viết app đơn giản
Viết ứng dụng đơn giản bằng java thông ra một api để có thể get được bằng postman

Ứng dụng được viết tương tự như video sau: 

`How to Create Spring Boot Project in IntelliJ | Community FREE Edition`

Ứng dụng này sẽ chạy ở cổng 8080 và khi gửi request đến API :

`/welcome`: “Hello world!”

`/download`: File text 1Mb

Tiếp theo ta build image với tên là: henrypham2801/datptdownload

và đóng lên docker hub để có thể tạo được pod

## Dựng pod từ app
Pod được dựng từ file deployment sau:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: testapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: testapp-deployment
  template:
    metadata:
      labels:
        app: testapp-deployment
    spec:
      containers:
      - name: testapp-deployment
        image: henrypham2801/datptdownload
        ports:
        - containerPort: 8080
```

Sau đó chạy lệnh: 

`kubectl apply -f <tên_file>  -n <tên_namespace>`

Vậy là hoàn thành việc tạo 3 app. Giờ ta có thể forward port ra ngoài để xem app có chạy ngon không và test lại

# Dựng pod backend phiên bản nâng cấp (Author: Thành)

## Deploy

Deployment: `Simpleapp.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: simpleapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: simpleapp-deployment
  template:
    metadata:
      labels:
        app: simpleapp-deployment
    spec:
      containers:
      - name: simpleapp-deployment
        image: jerapiblannett/loadbalancer-app-709c7
        ports:
        - containerPort: 8080
```

## APIs

Ứng dụng chạy ở cổng `8080`.

Ứng dụng trả response theo định dạng `text/json`.

| Method | Endpoint | Parameters | Resource bond | Description |
|:-------|:---------|:-----------|:--------------|:------------|
| GET    | `/api/v1/index` | None | None |Trả về string `Hello world`.|
| GET    | `/api/v1/pi?n=(int)` | $n\in(1,\infty)$ | CPU | Tính toán số $\pi$ với `n` chữ số sau số thập phân. |
| GET    | `/api/v1/recurse?n=(int)` | $n\in(1,24)$ | MEM | Tính toán với `n` lần đệ quy. |
| GET    | `/api/v1/randomfile?n=(int)` | $n\in(1,10000)$ | STO_IO | Đọc và gửi trả lại nội dung trong `n` file text kích cỡ 1KB. |
| GET    | `/api/v1/bigfile?n=(int)` | $n\in(1,1000)$ | STO_IO+NET_IO | Đọc và gửi trả lại nội dung trong `n` file text kích cỡ 5MB. |
| GET    | `/api/v1/compress?n=(int)&t=(int)` | $n\in(1,1000), t\in(1,\infty)$ | COMBO | Đọc nội dung trong `n` file text kích cỡ 5MB, nén lại sử dụng thuật toán nén LZMA với `t` luồng và gửi trả lại nội dung nén. |

# Dựng pod NGINX.

Sau khi có 3 pod backend, ta tiến hành dựng pod NGINX bằng deployment sau:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-deployment
  template:
    metadata:
      labels:
        app: nginx-deployment
    spec:
      containers:
      - name: nginx-deployment
        image: nginx
        ports:
        - containerPort: 80
        - containerPort: 8081
        volumeMounts:
        - name: nginx-config
          mountPath: /etc/nginx/conf.d
      volumes:
      - name: nginx-config
        configMap:
          name: nginx-config
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  datpt.conf: |
    upstream backend {
      server 10.233.102.205:8080;
      server 10.233.102.210:8080;
      server 10.233.102.212:8080;
    }
    server {
      listen 8081;
      server_name localhost;
      location / {
        proxy_pass http://backend/download;
      }
    }
```
`Lưu ý`: Thay config vào trong config map cho phù hợp, sau đó apply là được
# Load balancer project

## Đường dẫn báo cáo hàng tuần
https://drive.google.com/drive/folders/1f5jJhD2cjQhInBj-8sxMd62XWsat4NZ1d

## Mục đích
Mục đích cuối cùng của project là triển khai một thuật toán loadbalancer mới

## Ý tưởng
Thuật toán sẽ đươc sử dụng trong loadbalancer, sau đó lấy metric từ các server, sau đó chọn server để forward request

## Các bước thực hiện
- Xây dựng mô hình để test
- Xây dựng thuật toán
- So sánh tính ưu việt của thuật toán so với các thuật toán đã có

## Sơ lược mô hình để test
Mô hình test được mô tả trong hình sau:

![alt text](image.png)

Giải thích mô hình:

- `Jmeter`: Bắn request
- `LB`: Forward request (Nơi cài thuật toán)
- `App`: Nơi xử lý request
- `Monitoring`: Một nơi theo dõi được số liệu các server
### Jmeter
Là tool để mô phỏng client bắn request liên tục (Cài trên laptop cá nhân)

### LB
LB sử dụng Nginx, thuật toán mới sử dụng python, ý tưởng là sẽ dùng code để kiểm tra liên tục xem server nào còn thừa nhiều tài nguyên nhất, sau khi kiểm tra xong thì tạo 1 file config Nginx mới, sau đó ghi đè và reload lại config của Nginx là xong 
### App
App chạy ở cổng `8080`.

Ứng dụng trả response theo định dạng `text/json`.

| Method | Endpoint | Parameters | Resource bond | Description |
|:-------|:---------|:-----------|:--------------|:------------|
| GET    | `/api/v1/index` | None | None |Trả về string `Hello world`.|
| GET    | `/api/v1/pi?n=(int)` | $n\in(1,\infty)$ | CPU | Tính toán số $\pi$ với `n` chữ số sau số thập phân. |
| GET    | `/api/v1/recurse?n=(int)` | $n\in(1,24)$ | MEM | Tính toán với `n` lần đệ quy. |
| GET    | `/api/v1/randomfile?n=(int)` | $n\in(1,10000)$ | STO_IO | Đọc và gửi trả lại nội dung trong `n` file text kích cỡ 1KB. |
| GET    | `/api/v1/bigfile?n=(int)` | $n\in(1,1000)$ | STO_IO+NET_IO | Đọc và gửi trả lại nội dung trong `n` file text kích cỡ 5MB. |
| GET    | `/api/v1/compress?n=(int)&t=(int)` | $n\in(1,1000), t\in(1,\infty)$ | COMBO | Đọc nội dung trong `n` file text kích cỡ 5MB, nén lại sử dụng thuật toán nén LZMA với `t` luồng và gửi trả lại nội dung nén. |

### Monitoring
Testbed được thực hiện trên K8S, nên ta sẽ lấy metric từ K8S bằng helm của prometheus

## Xây dựng testbed

### Setup Jmeter
Tải jmeter cho Ubuntu bằng hướng dẫn sau:

https://linux.how2shout.com/2-ways-to-install-apache-jmeter-on-ubuntu-22-04-lts-linux/

### Cài đặt monitoring cho cụm (Chỉ cần setup 1 lần cho cụm)
Chạy các câu lệnh sau để cài helm prometheus:
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack
```

Để truy cập grafana của helm trên, sử dụng mật khẩu là `prom-operator`


### Cài đặt 3 pod backend và loadbalancer

Chạy câu lệnh sau:
```
kubectl apply -f TestbedManifest/
```

Câu lệnh trên sẽ cài đặt 3 pod backend và 2 loadbalancer, 1 loadbalancer được cài RoundRobin Nginx, cái còn lại thì là NGINX trống để có thể thực hiện thuật toán mới

Do NGINX để thực hiện thuật toán đang trống, ta cần cài các câu lệnh sau để NGINX có thể chạy được python
```
apt update
mkdir newAlgorithm
cd newAlgorithm
apt install -y python3 python3-pip python3.11-venv nano vim
python3 -m venv venv
source venv/bin/activate
pip3 install requests
```
Sau đó, ta copy file python để chạy thuật toán mới vào 1 file trong thư mục newAlgorithm
```
nano Algorithm-OFFICIAL.py
```
File python dùng để chạy nằm trong file `Algorithm-OFFICIAL.py`
Chạy file bằng câu lệnh:
```
python3 Algorithm-OFFICIAL.py 10.244.230.130:9090
```

Với `10.244.230.130:9090` là endpoint của prometheus-server

Sau đó, để nguyên cho pod nó chạy python, vậy là đã setup xong


<!-- ## Dựng testbed

Các files manifest được đặt tại `TestbedManifest/j12t`

1. Tạo các namespace: `j12t`, `j12t-monitoring`, `j12t-test`
2. Deploy `SimpleApp`: `kubectl apply -f simpleapp.yaml`
3. Deploy `Default-NGINX` (NGINX nguyên gốc): `kubectl apply -f default_nginx.yaml`
4. Deploy `Prometheus+Grafana`: `kubectl apply -f monitoring.yaml`
5. Deploy `Modified-NGINX` (NGINX đã chỉnh sửa để áp dụng các thuật toán): `kubectl apply -f modified_nginx.yaml` -->



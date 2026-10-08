# Thực hành buổi 1: Lập trình Python với MQTT

- Sinh viên: 
+Lê Huy Hải – B23DCCN272
+Phạm Thu Hà - B23DCCN267
+Nguyễn Thu Thảo - B23DCCN776
- Thư viện: `paho-mqtt` (hỗ trợ cả bản 1.x và 2.x)

## 1. Cấu hình MQTT broker

Mặc định dùng **broker công cộng HiveMQ**: `broker.hivemq.com`, cổng `1883` (không cần tài khoản).

> Broker công cộng dùng chung cho mọi người, nên topic có thể bị người khác gửi nhầm vào. Khi demo nên chạy broker cục bộ (xem bên dưới).

Cấu hình nằm trong file `config.py`:

| Thông số | Mặc định | Đổi bằng biến môi trường |
|---|---|---|
| Broker | `broker.hivemq.com` | `MQTT_BROKER` |
| Port | `1883` | `MQTT_PORT` |

Trước khi chạy, **sửa `STUDENT_NAME` và `STUDENT_ID`** trong `config.py`.

Dùng broker cục bộ (Mosquitto):

```bash
# Ubuntu/Debian: sudo apt install mosquitto
# Windows: tải tại https://mosquitto.org/download/
mosquitto -v

# Linux/macOS
export MQTT_BROKER=localhost
# Windows PowerShell
$env:MQTT_BROKER="localhost"
```

## 2. Cài đặt

```bash
pip install -r requirements.txt     # hoặc: pip install paho-mqtt
```

## 3. Cách chạy

Mỗi bài cần **mở 2 terminal**; chạy chương trình nhận (subscriber/device/monitor) **trước**.

### Bài 1 – Publisher / Subscriber cơ bản (topic `iot/lab/message`)

```bash
# Terminal 1
python subscriber_bai1.py
# Terminal 2
python publisher_bai1.py          # gửi 1 thông điệp
python publisher_bai1.py 5        # gửi 5 thông điệp liên tiếp
```

### Bài 2 – Cảm biến nhiệt độ/độ ẩm (topic `iot/lab/sensor01/data`)

```bash
# Terminal 1
python monitor_subscriber_bai2.py            # giám sát sensor01
# Terminal 2
python sensor_publisher_bai2.py              # gửi dữ liệu mỗi 3 giây
```

Mở rộng: `python sensor_publisher_bai2.py sensor02` và giám sát tất cả bằng `python monitor_subscriber_bai2.py all` (topic `iot/lab/+/data`).

Payload JSON: `{"device_id": "sensor01", "temperature": 28.5, "humidity": 65.2}`.
Cảnh báo: nhiệt độ > 35 °C → `CANH BAO: Nhiet do cao`; độ ẩm < 40 % → `CANH BAO: Do am thap`.

### Bài 3 – Điều khiển đèn thông minh

| Topic | Chiều | Nội dung |
|---|---|---|
| `iot/lab/light01/cmd` | Controller → Device | `ON` / `OFF` |
| `iot/lab/light01/status` | Device → Controller | `{"device_id":"light01","status":"ON"}` |

```bash
# Terminal 1
python device_bai3.py
# Terminal 2
python controller_bai3.py        # nhập ON, OFF; nhập EXIT để thoát
```

Mở rộng: truyền tên thiết bị làm tham số, ví dụ `python device_bai3.py fan01` và `python controller_bai3.py fan01` (topic `iot/lab/fan01/cmd|status`).

## 4. Kết quả đạt được

- Bài 1: publisher gửi họ tên, mã SV và lời chào lên `iot/lab/message`; subscriber in Topic, Payload, Time; chạy liên tục đến khi Ctrl+C; publisher gửi được nhiều thông điệp.
- Bài 2: sensor gửi JSON mỗi 3 giây; monitor phân tích JSON, in từng dòng và cảnh báo đúng ngưỡng; hỗ trợ nhiều cảm biến.
- Bài 3: điều khiển hai chiều qua `cmd`/`status`; device phản hồi trạng thái sau mỗi lệnh hợp lệ (có `retain` nên controller vào sau vẫn thấy trạng thái hiện tại); báo lỗi lệnh sai, hỗ trợ `EXIT`, hỗ trợ nhiều thiết bị.

## 5. Cấu trúc thư mục

```
config.py                    # cấu hình broker + thông tin sinh viên
publisher_bai1.py            subscriber_bai1.py
sensor_publisher_bai2.py     monitor_subscriber_bai2.py
device_bai3.py               controller_bai3.py
requirements.txt             README.md
```

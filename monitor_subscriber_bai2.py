"""Bai 2 - Monitoring Subscriber: nhan du lieu cam bien, kiem tra nguong canh bao.

Cach chay:
    python monitor_subscriber_bai2.py            # chi sensor01
    python monitor_subscriber_bai2.py sensor02   # mot thiet bi khac
    python monitor_subscriber_bai2.py all        # tat ca cam bien (iot/lab/+/data)
"""
import json
import sys

from config import BROKER, PORT, KEEPALIVE, make_client, connect_failed

TEMP_MAX = 35.0   # do C
HUMI_MIN = 40.0   # %

arg = sys.argv[1] if len(sys.argv) > 1 else "sensor01"
TOPIC = "iot/lab/+/data" if arg == "all" else f"iot/lab/{arg}/data"


def on_connect(client, userdata, flags, rc, properties=None):
    if connect_failed(rc):
        print(f"Ket noi that bai, ma loi: {rc}")
        return
    print(f"Da ket noi broker {BROKER}:{PORT}")
    client.subscribe(TOPIC)
    print(f"Dang giam sat topic: {TOPIC} (Ctrl+C de thoat)\n")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        device = data["device_id"]
        temp = float(data["temperature"])
        humi = float(data["humidity"])
    except (ValueError, KeyError, TypeError) as e:
        print(f"Payload khong hop le ({e}): {msg.payload!r}\n")
        return

    print(f"Device: {device}")
    print(f"Temperature: {temp} C")
    print(f"Humidity: {humi} %")
    if temp > TEMP_MAX:
        print("CANH BAO: Nhiet do cao")
    if humi < HUMI_MIN:
        print("CANH BAO: Do am thap")
    print()


def main():
    client = make_client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(BROKER, PORT, KEEPALIVE)
    except OSError as e:
        print(f"Khong ket noi duoc broker {BROKER}:{PORT} - {e}")
        sys.exit(1)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDa dung giam sat.")
        client.disconnect()


if __name__ == "__main__":
    main()

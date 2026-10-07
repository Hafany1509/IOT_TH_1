"""Bai 1 - Subscriber: lang nghe topic iot/lab/message, chay den khi Ctrl+C."""
import sys
from datetime import datetime

from config import BROKER, PORT, KEEPALIVE, make_client, connect_failed

TOPIC = "iot/lab/message"


def on_connect(client, userdata, flags, rc, properties=None):
    if connect_failed(rc):
        print(f"Ket noi that bai, ma loi: {rc}")
        return
    print(f"Da ket noi broker {BROKER}:{PORT}")
    client.subscribe(TOPIC, qos=1)
    print(f"Dang lang nghe topic: {TOPIC} (Ctrl+C de thoat)\n")


def on_message(client, userdata, msg):
    print("Nhan duoc message:")
    print(f"Topic: {msg.topic}")
    print(f"Payload: {msg.payload.decode('utf-8', errors='replace')}")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}\n")


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
        print("\nDa dung subscriber.")
        client.disconnect()


if __name__ == "__main__":
    main()

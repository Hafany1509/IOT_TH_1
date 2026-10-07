"""Bai 3 - Smart Light Device: nhan lenh ON/OFF, phan hoi trang thai.

Cach chay:
    python device_bai3.py            # light01
    python device_bai3.py fan01      # thiet bi khac (mo rong)
"""
import json
import sys

from config import BROKER, PORT, KEEPALIVE, make_client, connect_failed

DEVICE_ID = sys.argv[1] if len(sys.argv) > 1 else "light01"
CMD_TOPIC = f"iot/lab/{DEVICE_ID}/cmd"
STATUS_TOPIC = f"iot/lab/{DEVICE_ID}/status"

state = "OFF"  # trang thai ban dau


def publish_status(client):
    payload = json.dumps({"device_id": DEVICE_ID, "status": state})
    # retain=True: controller ket noi sau van biet trang thai hien tai
    client.publish(STATUS_TOPIC, payload, qos=1, retain=True)
    print(f"Da gui trang thai -> {STATUS_TOPIC}: {payload}")


def on_connect(client, userdata, flags, rc, properties=None):
    if connect_failed(rc):
        print(f"Ket noi that bai, ma loi: {rc}")
        return
    print(f"[{DEVICE_ID}] Da ket noi broker {BROKER}:{PORT}")
    client.subscribe(CMD_TOPIC, qos=1)
    print(f"[{DEVICE_ID}] Dang cho lenh tai {CMD_TOPIC} (Ctrl+C de thoat)")
    publish_status(client)


def on_message(client, userdata, msg):
    global state
    cmd = msg.payload.decode("utf-8", errors="replace").strip().upper()
    print(f"Nhan lenh: {cmd}")
    if cmd in ("ON", "OFF"):
        state = cmd
        print(f"[{DEVICE_ID}] Den chuyen sang: {state}")
        publish_status(client)
    else:
        print(f"Lenh khong hop le: {cmd!r} (chi chap nhan ON/OFF)")


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
        print("\nDa tat thiet bi.")
        client.disconnect()


if __name__ == "__main__":
    main()

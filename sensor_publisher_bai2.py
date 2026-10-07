"""Bai 2 - Sensor Publisher: gia lap cam bien gui nhiet do/do am moi 3 giay.

Cach chay:
    python sensor_publisher_bai2.py             # sensor01
    python sensor_publisher_bai2.py sensor02    # thiet bi khac (mo rong)
"""
import json
import random
import sys
import time

from config import BROKER, PORT, KEEPALIVE, make_client

INTERVAL = 3  # giay


def main():
    device_id = sys.argv[1] if len(sys.argv) > 1 else "sensor01"
    topic = f"iot/lab/{device_id}/data"

    client = make_client()
    try:
        client.connect(BROKER, PORT, KEEPALIVE)
    except OSError as e:
        print(f"Khong ket noi duoc broker {BROKER}:{PORT} - {e}")
        sys.exit(1)
    client.loop_start()
    print(f"[{device_id}] Da ket noi broker {BROKER}:{PORT}, gui du lieu moi {INTERVAL}s (Ctrl+C de thoat)")

    try:
        while True:
            payload = {
                "device_id": device_id,
                # Khoang rong hon muc binh thuong de thinh thoang kich hoat canh bao
                "temperature": round(random.uniform(25.0, 40.0), 1),
                "humidity": round(random.uniform(30.0, 80.0), 1),
            }
            client.publish(topic, json.dumps(payload), qos=0)
            print(f"Da gui -> {topic}: {json.dumps(payload)}")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nDa dung cam bien.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()

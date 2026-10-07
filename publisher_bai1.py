"""Bai 1 - Publisher: gui thong diep chao mung len topic iot/lab/message."""
import sys
import time

from config import BROKER, PORT, KEEPALIVE, STUDENT_NAME, STUDENT_ID, make_client, connect_failed

TOPIC = "iot/lab/message"


def main():
    # Tuy chon: python publisher_bai1.py 5  -> gui 5 thong diep lien tiep
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    client = make_client()
    try:
        client.connect(BROKER, PORT, KEEPALIVE)
    except OSError as e:
        print(f"Khong ket noi duoc broker {BROKER}:{PORT} - {e}")
        sys.exit(1)
    client.loop_start()
    print(f"Da ket noi broker {BROKER}:{PORT}")

    for i in range(1, count + 1):
        payload = f"Xin chao tu client Python MQTT - {STUDENT_ID} - {STUDENT_NAME}"
        if count > 1:
            payload += f" (#{i})"
        info = client.publish(TOPIC, payload, qos=1)
        info.wait_for_publish()
        print(f"Da gui -> Topic: {TOPIC} | Payload: {payload}")
        if i < count:
            time.sleep(1)

    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    main()

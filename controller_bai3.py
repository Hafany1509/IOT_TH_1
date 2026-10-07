"""Bai 3 - Controller App: nhap lenh ON/OFF tu ban phim, hien thi trang thai phan hoi.

Cach chay:
    python controller_bai3.py            # dieu khien light01
    python controller_bai3.py fan01      # dieu khien thiet bi khac (mo rong)
"""
import sys
import time

from config import BROKER, PORT, KEEPALIVE, make_client, connect_failed

DEVICE_ID = sys.argv[1] if len(sys.argv) > 1 else "light01"
CMD_TOPIC = f"iot/lab/{DEVICE_ID}/cmd"
STATUS_TOPIC = f"iot/lab/{DEVICE_ID}/status"


def on_connect(client, userdata, flags, rc, properties=None):
    if connect_failed(rc):
        print(f"Ket noi that bai, ma loi: {rc}")
        return
    client.subscribe(STATUS_TOPIC, qos=1)


def on_message(client, userdata, msg):
    print("\nTrang thai nhan duoc:")
    print(msg.payload.decode("utf-8", errors="replace"))
    print("Nhap lenh: ", end="", flush=True)


def main():
    client = make_client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(BROKER, PORT, KEEPALIVE)
    except OSError as e:
        print(f"Khong ket noi duoc broker {BROKER}:{PORT} - {e}")
        sys.exit(1)
    client.loop_start()
    time.sleep(1)  # cho nhan trang thai retained (neu co)
    print(f"Controller cho {DEVICE_ID} | Lenh hop le: ON, OFF, EXIT")

    try:
        while True:
            cmd = input("Nhap lenh: ").strip().upper()
            if cmd == "EXIT":
                break
            if cmd not in ("ON", "OFF"):
                print("Loi: lenh khong hop le, chi nhap ON, OFF hoac EXIT")
                continue
            client.publish(CMD_TOPIC, cmd, qos=1)
            print(f"Da gui lenh {cmd} toi {DEVICE_ID}")
            time.sleep(0.5)  # cho thiet bi phan hoi
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        print("\nThoat controller.")
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()

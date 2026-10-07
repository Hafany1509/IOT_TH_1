"""Cau hinh chung cho ca 3 bai thuc hanh MQTT."""
import os
import paho.mqtt.client as mqtt

# ====== SUA THONG TIN CUA BAN TAI DAY ======
STUDENT_NAME = "Le Huy Hai"
STUDENT_ID = "B23DCCN272"

# ====== CAU HINH BROKER ======
# Mac dinh dung broker cong cong HiveMQ. Co the doi bang bien moi truong:
#   MQTT_BROKER=localhost MQTT_PORT=1883 python subscriber_bai1.py
BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
PORT = int(os.getenv("MQTT_PORT", "1883"))
KEEPALIVE = 60


def make_client(client_id=""):
    """Tao MQTT client, tuong thich paho-mqtt 1.x va 2.x."""
    try:
        from paho.mqtt.client import CallbackAPIVersion
        return mqtt.Client(CallbackAPIVersion.VERSION2, client_id=client_id)
    except ImportError:  # paho-mqtt 1.x
        return mqtt.Client(client_id=client_id)


def connect_failed(rc):
    """True neu ma tra ve cua on_connect la loi (1.x: int, 2.x: ReasonCode)."""
    if hasattr(rc, "is_failure"):
        return rc.is_failure
    return rc != 0

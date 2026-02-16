import socket
import time
import pandas as pd

# ===============================
# CONFIGURACIÓN
# ===============================
UDP_IP = "192.168.1.107"   # Escuchar en todas las interfaces
UDP_PORT = 5005

# ===============================
# SOCKET UDP
# ===============================
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Escuchando en puerto {UDP_PORT}...")

data = []

start_time = time.time()

try:
    while True:
        print("Lectura de datos...")
        message, addr = sock.recvfrom(1024)
        recv_time = time.time()

        payload = message.decode().strip()
        packet_id, send_time_ms = payload.split(",")

        packet_id = int(packet_id)
        send_time_ms = int(send_time_ms)

        # Convertimos a segundos
        send_time = send_time_ms / 500.0

        latency = recv_time - start_time - send_time

        if packet_id:
            print(f"Paquete recibido: {packet_id}")
        data.append({
            "packet_id": packet_id,
            "send_time_s": send_time,
            "recv_time_s": recv_time - start_time,
            "latency_s": latency
        })

except KeyboardInterrupt:
    print("\nRecepción detenida.")

# ===============================
# DATAFRAME
# ===============================
df = pd.DataFrame(data)

print(df)
# Detectar paquetes perdidos
df["expected_id"] = range(df["packet_id"].iloc[0],
                           df["packet_id"].iloc[0] + len(df))
df["lost"] = df["packet_id"] != df["expected_id"]

print(df.head())

# Guardar resultados
df.to_csv("../Data/wifi_packets.csv", index=False)
print("Datos guardados en ../Data/wifi_packets.csv")

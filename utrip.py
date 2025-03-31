import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, medfilt

# Učitavanje podataka
time_path = "time.txt"
data_path = "data.txt"

with open(time_path, "r", encoding="utf-8") as f:
    timestamps = pd.to_datetime([t.strip() for t in f.readlines()])

with open(data_path, "r", encoding="utf-8") as f:
    bit_values = np.array([int(d.strip()) for d in f.readlines()])

# Pretvorba bitova u napon
voltage_values = (bit_values / 1023) * 5

# Kreiranje DataFrame-a
df = pd.DataFrame({"Time": timestamps, "Bits": bit_values, "Voltage": voltage_values})

# Filtriranje podataka nakon 14:19:40
df = df[df["Time"] >= pd.Timestamp("2025-03-25 14:19:40")].reset_index(drop=True)

# Primjena medijan filtra za uklanjanje šuma
df["Voltage"] = medfilt(df["Voltage"], kernel_size=5)

# Statički prag za detekciju vrhova
static_height = 2.0

# Pronalazak vrhova signala (otkucaji srca)
peaks, _ = find_peaks(df["Voltage"], height=static_height, distance=40)

# Izračun intervala između otkucaja (RR interval u sekundama)
rr_intervals = np.diff(df["Time"].iloc[peaks]).astype('timedelta64[ms]').astype(float) / 1000

# Izračun prosječnog BPM-a (broj otkucaja u minuti)
bpm = 60 / np.mean(rr_intervals) if len(rr_intervals) > 0 else np.nan

# Izračun HRV (standardna devijacija RR intervala)
hrv = np.std(rr_intervals) if len(rr_intervals) > 1 else np.nan

# Iscrtavanje signala s označenim otkucajima
plt.figure(figsize=(12, 6))
plt.plot(df["Time"], df["Voltage"], label="Voltage (V)")
plt.scatter(df["Time"].iloc[peaks], df["Voltage"].iloc[peaks], color='red', label="Heartbeats")
plt.xlabel("Time")
plt.ylabel("Voltage (V)")
plt.title("Measured Heart Signal")
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.show()

# Ispis rezultata
print(f"Average BPM: {bpm:.2f}")
print(f"Heart Rate Variability (HRV): {hrv:.2f} s")

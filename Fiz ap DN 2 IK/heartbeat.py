# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 19:09:40 2025

@author: OPenworldgamer
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import datetime

# Funkcija za nalaganje podatkov iz datotek
def load_data(data_file, time_file):
    # Naloži ADC vrednosti
    adc_values = np.loadtxt(data_file)
    
    # Naloži časovne oznake in jih pretvori v sekunde (relativno na prvo točko)
    with open(time_file, 'r') as f:
        time_lines = f.readlines()
    # Pretvori vsako vrstico v datetime objekt
    times = [datetime.datetime.fromisoformat(t.strip()) for t in time_lines if t.strip()]
    # Pretvori v sekunde glede na začetni čas
    t0 = times[0]
    time_seconds = np.array([(t - t0).total_seconds() for t in times])
    
    return adc_values, time_seconds

# Pretvori ADC vrednosti v napetost (0–5V) pri 10-bitni ločljivosti
def adc_to_voltage(adc_values):
    return adc_values * (5.0 / 1023)

# Glavni del programa
if __name__ == "__main__":
    # Naložimo podatke (datoteke "data.txt" in "time.txt" morajo biti v isti mapi)
    adc_values, time_sec = load_data("data.txt", "time.txt")
    voltage = adc_to_voltage(adc_values)
    
    # Zaznavanje R-valov s funkcijo find_peaks
    # Nastavimo minimalno višino (lahko prilagodite glede na signal) in minimalno razdaljo med vrhovi.
    # Tukaj uporabimo, npr., da je prag 2.0V, kar lahko ustreza vrhom EKG signala.
    peaks, properties = find_peaks(voltage, height=2.0, distance=100)
    
    # Izračun intervalov utripanja (v sekundah)
    rr_intervals = np.diff(time_sec[peaks])
    
    # Izračun srčnega utripa: povprečni interval med utripi in pretvorba v utrip na minuto (bpm)
    avg_rr = np.mean(rr_intervals)
    avg_hr = 60.0 / avg_rr if avg_rr > 0 else np.nan
    
    # Izračun variabilnosti srčnega utripa (npr. standardni odklon intervalov utripanja v milisekundah)
    hr_variability = np.std(rr_intervals) * 1000  # pretvorba v ms
    
    # Izpis rezultatov
    print(f"Povprečni srčni utrip: {avg_hr:.1f} bpm")
    print(f"Variabilnost srčnega utripa (SDNN): {hr_variability:.1f} ms")
    
    # Risanje grafa
    plt.figure(figsize=(12, 6))
    plt.plot(time_sec, voltage, label="EKG signal")
    plt.plot(time_sec[peaks], voltage[peaks], "rx", label="Utripi")
    plt.xlabel("Čas (s)")
    plt.ylabel("Napetost (V)")
    plt.title("EKG signal z zaznanim utripom")
    plt.legend()
    plt.xlim(0.0)
    plt.ylim(0.0)
    plt.grid(True)
    plt.savefig("EKG signal z zaznanim utripom.png")
    plt.show()

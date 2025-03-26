import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
# za animacijo
import matplotlib.animation as animation

fp="C:\\Users\\Leopold\\Desktop\\UMtemp"

# 1. Uvoz podatkov
with open(f'{fp}/data.txt', 'r') as f:
    v_bits = np.array([int(line.strip()) for line in f])

with open(f'{fp}/time.txt', 'r') as f:
    t_stmp = [line.strip() for line in f]

# 2. Pretvorba časovnega formata iz datoteke v za računanje primerne časovne korake (enote)
times = []
for ts in t_stmp:
    time_part = ts.split(' ')[1]  # Iz datoteke preberem prvi stolpec (čas:npr. "12:34:56")
    h, m, s = time_part.split(':') # razdelim na ure, minute, sekunde
    seconds = float(h) * 3600 + float(m) * 60 + float(s) # pretvorim vse skupaj v sekunde
    times.append(seconds)
times = np.array(times) - times[0]  # Relativni čas (sekunde)
#debug------------------------------------------------------------------|
#time_limit = 12  # seconds
#mask = times <= time_limit
#times = times[mask]
#-----------------------------------------------------------------------|

# samplanje (da vidimo koliko je frekvenca v Hz (debugganje))
samp_rate= len(times)/(times[-1]-times[0]) # Hz
print(f"Frekvenca vzorčenja: {samp_rate:.2f} Hz\n")

#debug------------------------------------------------------------------|
#assert len(v_bits) == len(times), "data ni enakih dimenzij kot time."
#print(len(times), len(v_bits))
#-----------------------------------------------------------------------|

# 3. Pretvorba bitov v mV
v_mV = (v_bits * 5000) / 1023  # Convert bits to mV (Če želim V, množim s 5, ne 5000)
#v_mV = v_mV[mask] # DEBUG: maskiranje signalov, da izbrišemo šum zredi meritve

# 4. Poiščem "vrhove" - maksimalne vrednosti filtriram, tako da zahtevam, da je signal vsaj 59%
# makismalne vrednosti napetosti in počakam nsalednjih 30-50 časovnih korakov, da ne preberem istega
# vrha in okolice 2x - Tole je treba prilagoditi glede na signal,
# ki ga imamo in eksperimentirati za optimalno delovanje
max_mV = np.max(v_mV)             # Max vrednost v mV
threshold = 0.59 * max_mV         # Set threshold to 59 % max voltaže (mV)
min_distance = int(.33*samp_rate)  # Minimalna razdalja med maksimumi (0.33 s ustreza maksimalni predvideni frekvenci ~ 180 bpm)
peaks, _ = find_peaks(v_mV, height=threshold, distance=min_distance)

# 5. Izračunam RR intervale (ang. SDNN)
peak_times = times[peaks]           # časi maksimumov
rr_intervals = np.diff(peak_times)  # Razlike med zaporednimi utripi (s)

# Odstranim RR intervale, ki niso smiselni (>1.5 s za utrip je mal too much, oz. 0.3 sekunde mal premal)
if len(rr_intervals) > 0: # sistem deluje dinamično in je aplikanilen za osebe z nizkimi in viskimi frekvencami srčnega utripa
    median_rr = np.median(rr_intervals)
    v_rr_mask = (rr_intervals > median_rr*0.5) & (rr_intervals < median_rr*1.5) # verjetni RR int
    c_rr = rr_intervals[v_rr_mask] # popucani RR int
else:
    cleaned_rr = np.array([])

print("Raw RR Intervali (s):\n\n", rr_intervals)
print("Filtrirani RR intervali (s):\n\n", c_rr)
print("Min RR (Raw):", np.min(rr_intervals) if len(rr_intervals)>0 else "Nema")
print("Min RR (filt):", np.min(c_rr) if len(c_rr)>0 else "Nea vem")
print("Max RR (Raw):", np.max(rr_intervals) if len(rr_intervals)>0 else "Ništa")
print("Max RR (filt):", np.max(c_rr) if len(c_rr)>0 else "Kaj te vem")
print("\n")

# Znova preračunam razlike s filtritanimi podatki
if len(c_rr)>=2:
    rr_diff_c = np.diff(c_rr)
else:
    rr_diff_c = np.array([])
# Tole je za drug pristop (ang. RMSSD) - Oba sta ok, ker 50 sekund pade skoraj v
# short-term rang, pod 50 pa v ultra-short, kjer je RMSSD bolj natančen
# vir: https://www.escardio.org/static-file/Escardio/Guidelines/Scientific-Statements/guidelines-Heart-Rate-Variability-FT-1996.pdf
rr_diff = np.diff(rr_intervals) # Razlike v sekundah
rr_diff_m=np.mean(rr_diff) # 0 je zelo ustaljen ritem, odstopanje od 0 pomeni: aritmija
mean_rr = np.mean(rr_intervals)
# Za mojo radovedno dušo -------------------------------------|
print(f"Povprečna delta med utripi: {rr_diff_m:.2f} s")
print(f"Povprečni RR interval: {mean_rr:.2f} s\n")

plt.plot(rr_diff, label='Razlike med RR intervali')
plt.xlabel('$N$')
plt.ylabel(r'$\Delta t$ [s]')
plt.title('Razlike med RR intervali')
#plt.savefig(f'{fp}/RR_diff.png', dpi=200)
plt.show()
plt.close()
# ------------------------------------------------------------|
# 6. Povprečni srčni utrip
if len(peak_times) >= 2:   
    t_time = peak_times[-1] - peak_times[0] # Skupni čas v sekundah
    h_r = (len(peaks) - 1) / t_time * 60    # Utrip na minuto (bpm)
else:
    h_r=0 # brez vrhov (press f to pay respects)
print(f"Povprečni srčni utrip: {h_r:.2f} bpm")

# 7. Variabilnost srčnega utripa (HRV)
# Dolgoročna variabilnost (SDNN)
if len(c_rr)>=2:
    sdnn = np.std(c_rr,ddof=1)*1000 # std RR intervalov v ms
else:
    sdnn=0 # Če ni dovolj podatkov, si al mrtu al pa ni dovolj podatkov
print(f"Variabilnost utripa (HRV - SDNN): {sdnn:.2f} ms")

# Kratkoročna variabilnost
if len(rr_diff_c)>=1: # RMSSD
    rmssd = np.sqrt(np.mean(rr_diff_c**2))*1000
else:
    rmssd=0
print(f"Variabilnost utripa (HRV - RMSSD): {rmssd:.2f} ms\n")

if sdnn > 80: print("Elena = Gucci")
elif 80 > sdnn > 50: print("Elena = Gucci-ish")
elif 50 > sdnn > 30: print("Elena = Cooked-ish")
elif 30 > sdnn > 10: print("Elena = Cooked")
else: print("Elena = Grilled, Deepfried, Burned, charred and Cremated")

# 8. Graf EKG signala
plt.plot(times, v_mV, label='EKG signal (mV)')
plt.plot(times[peaks], v_mV[peaks], 'ro', label='Maksi')
plt.xlabel('$t$ [s]')
plt.ylabel('$V$ [mV]')
plt.title('EKG Signal (in vrhovi)')
plt.legend()
#plt.savefig(f'{fp}/Ekg_signal.png', dpi=200)
plt.show()
plt.close()

# 9. Graf RR intervalov
plt.figure(figsize=(10, 4))
plt.plot(rr_intervals, 'ro', label='Nefiltrirani') # kaj bi zaj enega rukno nazaj, kaj si te ja nor ...
plt.plot(np.where(v_rr_mask)[0], c_rr, 'go', label='Filtrirani')
plt.title('Filtriranje RR intervalov')
plt.xlabel("$N$")
plt.ylabel('$t_{int}$ [s]')
plt.legend()
#plt.savefig(f'{fp}/RR_intervals.png', dpi=200)
plt.show()
plt.close()

# 10. Animacija spreminjanja frekvence srčnega utripa (Zanimivo, če ne drugega ...)
fig, ax = plt.subplots()
ax.set_xlabel("$t$ [s]")
ax.set_ylabel(r"$\nu$ [bpm]")
ax.set_title("Animacija frekvence srčnega utripa")
line, = ax.plot([], [], lw=2) # lw = line width
c_dot = None # Sledim rdeči piki

# podatki za animacijo
if len(c_rr) > 0:
    hr_vals = 60 / c_rr  # Pretvori RR intervale v bpm
    t_ps = peak_times[1:][v_rr_mask]  # Časovne točke za filtrirane podatke
else:
    hr_values = np.array([])
    time_points = np.array([])

# območja osi
ax.set_xlim(t_ps[0] if len(t_ps)>0 else 0,
            t_ps[-1] if len(t_ps)>0 else 10)
ax.set_ylim(0, 180)

# inicializiram animacijo
def init():
    line.set_data([], [])
    return line,

# posodobim anim
def animate(i):
    global c_dot
    x = t_ps[:i+1]
    y = hr_vals[:i+1]
    line.set_data(x,y)

    # vizualna povratna info za vsak utrip
    # odstrani prejšnjo piko, če obstaja
    if c_dot:
        c_dot.remove()
    
    # Dodaj novo piko
    if len(x) > 0 and len(y) > 0:
        c_dot, = ax.plot(x[-1], y[-1], 'ro')

    return line,

# ustvari anim
if len(hr_vals)>0:
    ani = animation.FuncAnimation(
        fig,
        animate,
        frames=len(hr_vals),
        init_func=init,
        interval=70,
        blit=False,
        repeat=True
    )
    #ani.save(f'{fp}\\dhr.mp4', writer='ffmpeg', fps=10) # Rabiš ffmpeg
    plt.show()
else:
    print("Ni podatkov za animacijo!")
plt.close()

# 11. EKG-RT animacija
fig, ax = plt.subplots(figsize=(12, 4))
ax.set_xlabel("$t$ [s]")
ax.set_ylabel("$V$ [mV]")
ax.set_title("EKG v realnem času")

# Inicializacija
line, = ax.plot([], [], lw=1)
current_peak = ax.plot([], [], "ro", alpha=0)[0]  # Trenutni maks
display_window = 5 # Okno prikaza RT anim v sekindah (5 sekundni int)

# Data za anim
x_data = np.array([])
y_data = np.array([])
peaks_displayed = np.array([], dtype=int)

# Postavim osi
ax.set_xlim(0, display_window)
ax.set_ylim(np.min(v_mV)-100, np.max(v_mV)+100)

def init():
    line.set_data([], [])
    current_peak.set_data([], [])
    return line, current_peak

def animate(frame):
    global x_data, y_data, peaks_displayed
    
    # Postopen prikaz podatkov kot na realnem EKG
    x_data = times[:frame+1]
    y_data = v_mV[:frame+1]
    
    # Posodobim prikaz
    line.set_data(x_data, y_data)
    
    # Preverim, če imam nove makse
    current_peaks = peaks[peaks <= frame]
    new_peaks = current_peaks[~np.isin(current_peaks, peaks_displayed)]
    
    # Posodobim prikaz trenutnega maksa
    if len(new_peaks) > 0:
        peaks_displayed = np.union1d(peaks_displayed, new_peaks)
        current_peak.set_data(times[new_peaks], v_mV[new_peaks])
    
    # Prilagodim okno prikaza
    current_time = times[frame] if frame < len(times) else times[-1]
    ax.set_xlim(max(0, current_time - display_window), 
               max(display_window, current_time))
    
    return line, current_peak

# Interval računam glede na ffrekvenco vzorčenja
frame_interval = (1/samp_rate) * 1000  # ms na korak

# Ustvari anim
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=len(times),
    init_func=init,
    interval=frame_interval,
    blit=True,
    repeat=False
)
#ani.save(f'{fp}\\ekg_rt_animation.mp4', writer='ffmpeg', fps=samp_rate)
plt.show()
plt.close()  # plt.close() = Preventiva za prikaz v notebooku (ipynb),
             # če uvozim npr. "from matplotlib import rcParams",
             # ko se izdeluje predstavitev ipd.
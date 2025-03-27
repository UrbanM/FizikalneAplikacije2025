# Analiza EKG signala
V datoteki EKG.py je pythonova skripta za analizo in vizualizacijo signalov EKG (elektrokardiograma), in izračun variabilnosti srčnega utripa (heart rate variability (ang. HRV)).

## Kaj program dela (podrobno)
- Vizualizacija EKG signalov v realnem času (EKG-RT).
- Izračun frekvence srčnega utripa in animacija spreminjanja frekvence srčnega utripa (niha s časom).
- Analiza "RR" intervalov (intervalov med zaporednima srčnima utripoma).
- Analiza variabilnosti srčnega utripa (HRV) z dvema najpogostejšima načinoma:
    - SDNN (Standard Deviation of NN intervals).
    - RMSSD (Root Mean Square of Successive Differences).
- Filtriranje signalov in detekcija maksimumov.
- Progresivna vizualizacija delovnega postopka (grafi so v enakem zaporedju, kot je tekel miselni proces, da smo prišli do končnega rezultata).

## Knjižnice
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import matplotlib.animation as animation
```

## Obvezne Datoteke
- `data.txt` - EKG voltaže v bitih
- `time.txt` - Časovni podatki v formatu UU:MM:SS.ssssss

## Rezultati
- Tri slike:
    - `RR_diff.png`: Sprememba v intervalu RR,
    - `Ekg_signal.png`: EKG signal z maksimumi,
    - `RR_intervals.png`: RR interval.
- `.mp4` datoteka z animacijo spreminjanja frekvence srčnega utripa.
- `.mp4` datoteka z animacijo EKG signala v realnem času.

## Uporaba
1. Datoteke z EKG signali in časovnimi žigi uvozimo v python iz poljubnega mesta (posodobi variablo `fp` v EKG.py!).
2. Poženi skripto.
```bash
python EKG.py
```

## Pregled delovanja
1. Uvoz datotek.
2. Pretvorba EKG signala iz bitov v napetost
3. Zaznava maksimumov (vrhov) s dinamičnim prilagajanjem meje, nad katero še zaznamo vrh.
4. Izračun in filtriranje RR intervalov.
5. Izračun HRV.
6. Vizualizacija in animacija podatkov.

## Vir
- [Heart Rate Variability Standards 1996](https://www.escardio.org/static-file/Escardio/Guidelines/Scientific-Statements/guidelines-Heart-Rate-Variability-FT-1996.pdf)

## Misc
- Animacije in grafi so kot datoteke dostopne tudi v mojem branchu.
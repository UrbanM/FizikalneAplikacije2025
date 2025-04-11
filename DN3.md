# EKG Analiza za stannja: Normalno, hiperventilacija in relaksacija

## Opis

Python uporabimo za analizo EKG signalov, ki smo jih zajeli med normalnim dihanjem, hoperventilacijo in relaksacijo po hiperventialiciji. Potek obdelave je sledeč:
1.  Preberemo EKG podatke iz `.npy` datotek.
2.  Apliciramo različne pasovne filtre (Fourier, Butterworth, FIR).
3.  Vizualiziramo učunkovistost filtrov.
4.  Detekcija R-R vrhov in izračun povprečnega EKG signala.
5.  Izračun HRV (SDNN, RMSSD) in povprečnega srčnega utripa (BPM) za različne faze v eksperimentu: (normalno dihanje, hiperventilacija, relaksacija).

**Opomba:** Kodo bi se dalo zoptimizirati, vendar zaradi pomanjkanja časa tokrat to izpustimo.

## Delovanje

* Prebere EKG signal iz (`.npy`) datotek.
* Aplicira 3 vrste pasovnih filtrov.
* Generira primerjalne grafe.
* Zazna R-vrhove.
* Izračuna povprečne EKG signale okrog R-vrhov.
* Izračuna povprečne vrednosti BPM (RMSSD in SDNN).
* Shrani rezultate v različne datoteke in mape.

## Predvidena struktura delovnega okolja

Main.py pirčakuje sledečo strukturo:

Poljubna delovna mapa/[Analiza_ekg2.py, /fun[filters.py, izris.py, RR.py, HRVBPM.py, Testi.py, *.npy]]

## Pričakovane knjižnice

Slede knjižnice so obvezne za popolno delovanje skript:

* NumPy (`pip install numpy`)
* SciPy (`pip install scipy`)
* Matplotlib (`pip install matplotlib`)
* NeuroKit2 (`pip install neurokit2`)

## Vhodni podatki

* Vhodni EKG signal je v `.npy` formatu in se nahaja v mapi `fun/`.
* Skripta pričakuje, da je v `.npy` datoteki ali:
    * Matrika oblike: `'Time (s)'` in `'Input 1 (V)'`.
    * Navaden np array s podatki o amplitudi in času.
    * TKoda obravnava obba primera (ker nisem vedel kaka je zalčetna struktura, sem moral implementirati obe možnosti, od katerih je načeloma prava 1.).
* Modul `HRVBPM.py` privzame **statične in predhodno definirane pogoje faz dihanja**:
    * 0 - 120 seconds: Normalno dihanje
    * 120 ~ 200 seconds: Hiperventilacija
    * 200 - do konca: Relaksacija (normalno dihanje)
* Predvidena frekvenca vzorčenja (razvidna tudi iz .txt datoteke) je **1000 Hz**.

## Kako uporabiti programe

1.  Glej, da so knjižnice posnete in uvožene.
2.  pripravi delovno okolje (mapo).
3.  Vstavi `.npy` datoteke v mapo `fun/`.
4.  Prestavi se s konzolo v `Projektna_mapa/`.
5.  Poženi main.py:
    ```bash
    python Analiza_ekg2.py
    ```

## Moduli

1.  **`Analiza_ekg2.py`:**
    * Nadomesti main.py.
    * identificira `.npy` datoteke v mapi `fun/`.
    * Kliče `filters.py` za filtriranje signalov s `Fourier`, `Butterworth` in `FIR` metodami,ter shrani rezultate v `filtered_data/`.
    * Kliče `izris.py` za izris nefiltriranih signalov (`grafi_npy`) in primerja filtre (`plot_filter_comparison`).
    * Kliče `RR.py` (`RRpd`) za detekcijo R-vrhov in izračuna povprečne vrednosti EKG filtriranih podatkov ter jih shrani v `RRints/`.
    * Kliče `HRVBPM.py` (`hrvbpm`) za analizo HRV in BPM za fiksne faze dihanja, in shrani rezultate v `Phase_Analysis/`.

2.  **`fun/filters.py`:**
    * Vključuje funkcije `fourier`, `butterworth`, and `fir` pasovnih filtrov.
    * Tu so zapisani tudi ključni  parametri filtrov, kot sta najvišja in najnižja še dovoljena frekvenca.

3.  **`fun/izris.py`:**
    * `grafi_npy`: Nariše nefiltrirane EKG signale iz datotek `.npy`.
    * `plot_filter_comparison`: Primerjava filtrov.

4.  **`fun/RR.py`:**
    * `RRpd`: procesira datoteke iz `filtered_data/`. Izračuna RR intervale in povprečne vrednosti EKG ter jih shrani v `RRints/`.

5.  **`fun/HRVBPM.py`:**
    * `hrvbpm`: procesira datoteke iz `filtered_data/`.
    * Uporablja časovne točke (120s -> 200s -> konec) za definicijo intervalov 'Pred_HVL', 'HVL', in 'Po_HVL'.
    * Shrani podatke v `Phase_Analysis/results_*.txt` in grafe s prikazanimi fazami v `Phase_Analysis/phase_detection_*.png`.

## Output

Programi generairajo sledeče datoteke v mapi `Delovno_okolje/`:

* **`filtered_data/`**: Filtrirani EKG signali.
* **`RRints/`**: Mapa z:
    * `avg_ecg_*.npy`: Povprečnimi EKG signali okrog R-vrhov.
    * `validation_*.png`: Detekcijo R-vrhov.
* **`Phase_Analysis/`**: Mapa z:
    * `results_*.txt`: .txt datoteke s povprečnim utripom, SDNN in RMSSD za vsako fazo posebej (Pred_HVL, HVL, Po_HVL) za vse preocesirane datoteke.
    * `phase_detection_*.png`: vizualizacija faz na grafu frekvenc.
* **`filter_comparison_*.png`**: Grafi za primerjavo.

## Omejitve

* Pristop se da pohitriti in optimizirati. V programu so ostanki, ki jih je predlagal Chat in jih nisem popolnoma odstranil zaradi časovnih omejitev (to se nanaša predvsem na nalogo 3 (zadnja klicana funkcija, ki sem jo poskusil prilagoditi, tako da bi dinamično zaznavala spremembo faz, vendar mi ni uspelo - v prihodnje mislim, da bom to popravil in objavil novo datoteko))
* Neberljiva koda (nametane funckije povsod, ker jih nisem sproti zlagal, ampak sem jih pisal dinamično (verjetno je kakšna, ki sploh ni v uporabi, sploh od takrat, ko sem začel vzporedno uporabljati še GPT et. al.)).
* Statistična analiza iz modula `Testi.py` zaradi pomanjkanja podatkov ni uporabljena.
* Razlog: poiskusil sem nekoliko drugačen pristop k modeliranju sistema - podoben, kot v Visual Studio in ugotovil, da potrebujem še veliko prakse s takšno bravnavo problemov.

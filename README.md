# FizikalneAplikacije2025

## Naloga 1
Monty-Hallov "problem" je igra, v kateri si na začetku izberemo naključno število, navadno med 1 in 3, kar so v večini primerov oznake vrat, za katerimi se skrivata 2 kozi in 1 nagrada. Po prvi izbiri narator izbere naključna vrata -- tista, ki smo jih izbrali mi ali ne -- in vpraša, če bi si slučajno premislili. Tukaj nastopi "twist" igre, ki najprej ni očiten, saj mi ne vemo, katera vrata je narator v resnici odprl. Vemo le, da je odprl vrata, za katerimi je žival. Po premisleku ugotovimo, da je najbolj optimalno izbrati drugo opcijo, torej da si premislimo, saj imamo tako 1/2 možnosti, da pravilno uganemo, medtem ko v primeru, da vztrajamo pri svoji odločitvi, imamo 1/3 možnosti, da je odločitev prava.

## Naloga 2
Analiza EKG signalov je izjemnega pomena za napoved trenutnega stanja (zdravja) srca. Z EKG si pomagamo pri identifikaciji srčnih obolenj, kot je npr. aritmija, pomembna pa je predvsem napoved zdravja na dolgi rok, kjer pride v poštev tudi variabilnost srčnega utripa (HRV - Heart Rate Variability). HRV je pomembna v smislu, da nam med drugim pomaga identificirati naslednje: Naspanost, stres in afiniteto za zgodnja srčna obolenja. Nizka vrednost HRV (pod 20 ms) zahteva pregled pri zdravniku (počitek, visok stres ali bolezen). Med 30 in 50 ms je načeloma še sprejemljivo, vendar na dolgi rok zaskrbljujoče. Med 50 in 80 je povprečje zdravih posameznikov. Nad 80 ms so ljudje, ki se redno, vendar ne profesionalno, ukvarjajo s športom. Posamezniki s HRV Nad 100 ms so navadno profesionalni športniki, vojaki in fizično aktivni (vitalni) ljudje (glede na vir (`Reference`)).

Iz podatkov v `data.txt` in `time.txt` se da marsikaj nazorno pokazati, na primer:
- Potek EKG v realnem času.
- Intervali RR (med dvema zaporednima utripoma).
- Filtriranje signalov (Če imamo veliko šumov in anomalij)
    - Naš primer ima npr. minimalno vrednost med dvema zaporednima utripoma okrog 0.3 s, najdaljšo pa 2.2 s, kar ni mogoče, razen če srce popušča (analizirati bi moral na primer nekdo, ki je strokovnjak, da bi lahko ocenil ali je šum na srcu ali na merilni napravi ali problem v merilni tehniki).
    - Koda, s katero si pomagamo pri analizi prekomerno odstopajočih (nerealnih) vrhov je v glavnem sledeča (podobna):

    ```python
    print("Min RR (Raw):", np.min(rr_intervals) if len(rr_intervals)>0 else "/")
    print("Min RR (filt):", np.min(c_rr) if len(c_rr)>0 else "/")
    print("Max RR (Raw):", np.max(rr_intervals) if len(rr_intervals)>0 else "/")
    print("Max RR (filt):", np.max(c_rr) if len(c_rr)>0 else "/")
    ```
- HRV meritve na dva načina:
    - SDNN (Standard deviation of NN intervals). Izjemno uporabna tehnika pri dolgih časovnih intervalih, npr. 24 h (zajame hitre in počasne oscilacije).
    - RMSSD (Root Mean Square of Successive Differences). Tehnika, ki jo uporabljamo za kratke časovne razpone (navadno merimo 5 minut, ampak deluje tudi pri krajših meritvah). Izjemno občutljiva tehnika na spremembe med zaporednimi utripi.

### Dodatek
Na EKG izrisu se lepo vidijo količine (pojavi), ki jih velikokrat označujemo s črkami P, Q, R, S in T (glej sliko `hrvinternet.jpg`).
- P: Pred ostrim skokom (vrhom) opazimo majhen naraščaj v napetosti, kar predstavlja atrialno depolarizacijo (električna aktivacija atrija).
- Q: Napetost pade v negativ glede na referneco (0), in ponazarja depolarizacijo ventrikla (prekata).
- R: Glavni del cikla (utripa ali kompleksa QRS), ki pripada glavni električni aktivaciji prekatov.
- S: padec pod referenco po glavni električni aktivaciji (R) - Nadaljevanje depolarizacije prekatov.
- T: majhen naraščaj v električnem potencialu, ki pripada repolarizaciji ventriklov (prekati se "resetirajo" in začne se nov cikel (utrip)).

Pozicije PQRST so odvisne od frekvence srčnega utripa, stanja srca in velikosti srca. Časovni intervali; PR ~ 100-200 ms, QT ~ 300-450 ms {skupaj $\Tau\approx (600-800)$ ms}. (`Reference`)

## Reference
1. [HRV (1996)](https://www.escardio.org/static-file/Escardio/Guidelines/Scientific-Statements/guidelines-Heart-Rate-Variability-FT-1996.pdf).

2. [Electrocardiography](https://www.merckmanuals.com/en-ca/professional/cardiovascular-disorders/cardiovascular-tests-and-procedures/electrocardiography).